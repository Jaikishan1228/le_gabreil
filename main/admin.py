from django.contrib import admin
from .models import *

# Register your models here.
class MenuAdmin(admin.ModelAdmin):

    search_fields =('name',)
    list_filter = ('is_draft','date_created')
    list_display=("name","date_created","last_modified","is_draft")
    
    actions = ('publish',)
    
    def get_ordering(self,request):
        if request.user.is_superuser:
            return ('name','-date_created')
        return ('name',)
    
    def publish(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request,'{} published Successfully.'.format(count))
    publish.short_description = "publish selected items"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'approved')
    list_filter = ('complete', 'approved')
    search_fields = ('id', 'customer__name')
    ordering = ('-date_ordered',)
    readonly_fields = ('date_ordered',)

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'date_added')
    list_filter = ('order',)
    search_fields = ('id', 'product__name', 'order__customer__name')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)

    def has_change_permission(self, request, obj=None):
        """
        Disable editing of order items by non-superusers.
        """
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Disable deleting of order items by non-superusers.
        """
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'email', 'category', 'enrollment')
    search_fields = ('user__username', 'user__email', 'name', 'phone_number', 'email')
    
class StatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'time_needed', 'status')
    list_filter = ('status',)
    search_fields = ('order__id',)  # Assuming that Order model has an 'id' field

    
admin.site.register(Menu, MenuAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address)
admin.site.register(Status, StatusAdmin) 