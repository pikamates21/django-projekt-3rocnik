from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Employee, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'email', 'phone', 'photo_tag')
	readonly_fields = ('photo_tag',)

	def photo_tag(self, obj):
		if obj.photo:
			try:
				return format_html('<img src="{}" style="max-height:80px;"/>', obj.photo.url)
			except Exception:
				return ''
		return ''

	photo_tag.short_description = 'Foto'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name', 'employee_id', 'gender', 'start_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'customer', 'worker', 'created_at', 'final_price')