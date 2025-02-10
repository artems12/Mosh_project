from django.contrib import admin
from .models import InventoryItem, Category, Name, Supplier

#admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Name)
admin.site.register(Supplier)
