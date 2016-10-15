from django.contrib import admin
from .models import Product, ProductImage
# Register your models here.



class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	max_num = 10
	min_num = 1
class ProductAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'price']
	inlines = [
		ProductImageInline,
	]
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)