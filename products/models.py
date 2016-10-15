from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify


# Create your models here.
#We use this to only show active products when someone make a query to products
class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self.db)
 
	def all(self, *args, **kwargs):
		return self.get_queryset().active()


class Product(models.Model):
	title = models.CharField(max_length=120)
	active = models.BooleanField(default = True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	description = models.TextField(blank = True, null=True)

	def __unicode__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse("product_detail", kwargs= {"pk": self.pk})

	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		else:
			return img

def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	file_extension = filename.split(".")[1]
	new_filename = "%s.%s" %(instance.id, file_extension)
	return "products/%s/%s" %(slug, new_filename)

class ProductImage(models.Model):
	image = models.ImageField(upload_to = image_upload_to)
	product = models.ForeignKey(Product)

	def __unicode__(self):
		return self.product.title
