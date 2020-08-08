from django.db import models
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
import uuid
import cv2
# from admin.models import User

class Image(models.Model):
    image_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    image_height = models.PositiveIntegerField()
    image_width = models.PositiveIntegerField()
    image_source = models.ImageField(upload_to='images', height_field='image_height', width_field='image_width')
    # provider_id = models.CharField(max_length=20, null=True)
    original_image = models.ImageField(upload_to='original_image', null = True)
    

class Annotation(models.Model):
    annotation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_id = models.ForeignKey('Image', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    coordinates_x = ArrayField(models.IntegerField(), null = True)
    label = models.CharField(max_length=300)
    coordinates_y = ArrayField(models.IntegerField(), null = True)
    def __str__(self):
        return self.label

def resize(sender, instance, *args, **kwargs):
        if instance.image_source:
            if (min(instance.image_height, instance.image_width)<200):
                dim = None
                #print(instance.image_source.path)
                if (instance.image_height < 200 and instance.image_width>=instance.image_height):
                    
                    r = float(200/instance.image_height)
                    dim = (int(instance.image_width * r), 200)
                    instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
                elif (instance.image_width < 200 and instance.image_height>instance.image_width):
                    r = float(200/instance.image_width)
                    dim = (200,int(instance.image_height*r))
                    # print(dim)
                    instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
            if (max(instance.image_height, instance.image_width)>600):
                dim = None
                print(instance.image_source.path)
                if (instance.image_height > 600 and instance.image_width<instance.image_height):
                    
                    r = float(600/instance.image_height)
                    dim = (int(instance.image_width * r), 600)
                    instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    instance.image_source = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    
                elif (instance.image_width > 600 and instance.image_height<instance.image_width):
                    r = float(600/instance.image_width)
                    dim = (600,int(instance.image_height*r))
                    # print(dim)
                    instance.original_image = instance.image_source
                    imgUMat = cv2.imread(instance.image_source.path)
                    resized = cv2.resize(imgUMat, dim, interpolation = cv2.INTER_LANCZOS4)
                    cv2.imwrite(instance.image_source.path, resized)
            
            # instance.image_source = get_thumbnail(instance.image, '500x600', quality=99, format='JPEG')
            # instance.image_source =
        # super(Image, instance).save(*args, **kwargs)
        # instance.image_height=dim[1]
        # instance.image_width=dim[0]
        # instance.save()
        # instance.image_width.save()

post_save.connect(resize, sender=Image)