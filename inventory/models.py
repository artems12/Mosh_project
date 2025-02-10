from django.db import models
from django.contrib.auth.models import User



class InventoryItem(models.Model):
	name = models.ForeignKey('Name', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	category = models.ForeignKey('Category', on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

class ApplicationItem(models.Model):
	name = models.ForeignKey('Name', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	category = models.ForeignKey('Category', on_delete=models.CASCADE)
	comment = models.CharField(max_length=300)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

class PlanItem(models.Model):
	name = models.ForeignKey('Name', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	category = models.ForeignKey('Category', on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, blank=True, null=True)

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name


class Name(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'names'

	def __str__(self):
		return self.name

class Supplier(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'suppliers'

	def __str__(self):
		return self.name