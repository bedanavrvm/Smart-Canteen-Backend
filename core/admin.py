from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MenuItem, Order, OrderItem, Payment, Notification, Inventory, Tag

# Register your models here.

#This class customizes how your User model appears and behaves inside the Django Admin Dashboard.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'reg_number', 'email', 'role', 'is_staff', 'is_active', 'last_login')
    list_filter = ('role', 'is_staff', 'is_active', 'gender')
    search_fields = ('reg_number', 'name', 'email', 'phone_number')
    ordering = ('reg_number',)

    fieldsets = (
        (None, {'fields': ('reg_number', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'phone_number', 'gender', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'reg_number', 'name', 'email', 'phone_number', 'gender',
                'role', 'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )

admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Inventory)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_type', 'created_at')
    list_filter = ('tag_type',)
    search_fields = ('name', 'description')


######Showing Order Items in the Order View

class OrderItemInline(admin.TabularInline):  # or StackedInline
    model = OrderItem
    extra = 0  # don’t show extra empty rows by default

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__name',)
    inlines = [OrderItemInline]  # 👈 attaches items inside the order view

    def get_items(self, obj):
        return ", ".join([f"{i.menu_item.name} x{i.quantity}" for i in obj.items.all()])
    get_items.short_description = "Ordered Items"