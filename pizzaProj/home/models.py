from django.db import models
from django.contrib.auth.models import User

# Library Import: Model class: Pizza: 
# image resizing required-library
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Library Import: Model class: Order
import string, random
from django.dispatch import receiver
from django.db.models.signals import post_save  # this method works immedietly after inserting any record to DB
from channels.layers import get_channel_layer   # to get all the channel-layers
from asgiref.sync import async_to_sync
import json



# Models-class: Pizza    
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    image = models.ImageField(upload_to='pizzaImges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Pizza'
        ordering = ('name',)
        index_together = ( ('id', 'name') )


    def __str__(self) -> str:
        return self.name
    
    # Image resizing before uploading a pizza-image
    def save(self):
		#Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

		#Resize/modify the image (width,height)
        im = im.resize( (800,500) )

		#after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

		#change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Pizza,self).save()

    # static-method/ signals


# Models-class: Order
# This method will generate a random-string of 20 chars.
def random_string_generator(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = [
    ('Order Received by Restaurant', 'Order Received by Restaurant'),
    ('Baking', 'Baking'),
    ('Baked', 'Baked'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Order Received by Customer', 'Order Received by Customer'),
]

class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=CHOICES, default='Order Received by Restaurant')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order'
        ordering = ('-date',)

    def __str__(self) -> str:
        return self.order_id

    # overriding 'save' method to generate random-string while creating an order-record
    def save(self, *args, **kwargs):
        # If no 'order_id' isn't passed while creating an order.
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order, self).save(*args, **kwargs)


    # give the order-id as param whenever this-model-class-method is called & get the order-details.
    # used in the 'consumers.py' to get the current info of that specific-order.
    # The func is used inside the 'consumers.py' file's 'connect()' func.
    # Whenever this func gets called, it'll return the specific order-data by making query.
    # THIS METHOD SERVES THE SPECIFIC ORDER RECORD.
    @staticmethod
    def get_order_detail(order_id):
        instance = Order.objects.filter(order_id=order_id).first()
        data = {
            'order_id': instance.order_id,
            'amount': float(instance.amount),   # the Decimal type is not able to be serialized directly into JSON.
            'status': instance.status,
        }

        # Make a progress-percentage based on the 5-types of order-status
        progress_percentage = 0
        if instance.status == 'Order Received by Restaurant':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for Delivery':
            progress_percentage = 80
        elif instance.status == 'Order Received by Customer':
            progress_percentage = 100
        
        data['progress'] = progress_percentage  # extending the data-dict, which will also be used in the consumer-class ("OrderProgress")

        return data




# Post-save signal for Order-model-class
# Only works for [ ORDER-UPDATION ]
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    # If no new record is created, means the old records are updated/ modified, then execute the next block of code.
    # 'sender' is the order-model-class & 'instance' is the individual-order-record.
    if not created:
        data = {
            'order_id': instance.order_id,
            'amount': float(instance.amount),   # the Decimal type is not able to be serialized directly into JSON.
            'status': instance.status,
        }

        # Make a progress-percentage based on the 5-types of order-status
        progress_percentage = 0
        if instance.status == 'Order Received by Restaurant':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for Delivery':
            progress_percentage = 80
        elif instance.status == 'Order Received by Customer':
            progress_percentage = 100
        
        data['progress'] = progress_percentage  # extending the data-dict, which will also be used in the consumer-class ("OrderProgress")


        # Send this "data-dict" to the 'order_status' channel of the 'OrderProgress' consumer.
        channel_layer = get_channel_layer() # fetch all the channel layers

        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,
            {
                'type': 'order_status',
                'value': json.dumps(data),  # converts the python-dict into json-string-object
            }
        )
