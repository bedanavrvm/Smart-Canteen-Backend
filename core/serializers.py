from rest_framework import serializers
from .models import User, MenuItem, Order, OrderItem, Payment, Notification, Inventory, Tag


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone_number',
            'password',
            'name',
            'reg_number',
            'role', ''
            'profile_picture',
            'gender',
            'is_active',
            'is_staff',
        ]
        read_only_fields = ['is_staff', 'is_active', 'id']

    #Overriding the create() method
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.username = validated_data.get('reg_number')
        user.set_password(password)
        user.save()
        return user
    
    #Overriding the update() method
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'tag_type', 'description']


class MenuItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        write_only=True, 
        required=False,
        source='tags'
    )
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'availability', 
                  'image_url', 'tags', 'tag_ids', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        menu_item = MenuItem.objects.create(**validated_data)
        menu_item.tags.set(tags)
        return menu_item
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        
        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags if provided
        if tags is not None:
            instance.tags.set(tags)
        
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_image = serializers.ImageField(source='menu_item.image_url', read_only=True)
    price = serializers.DecimalField(source='menu_item.price', max_digits=10, decimal_places=2, read_only=True)
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menu_item',
        write_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'menu_item_name', 'menu_item_image', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_data = serializers.ListField(write_only=True, required=False)
    total_amount = serializers.DecimalField(source='total_price', max_digits=10, decimal_places=2, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'total_amount', 'status', 'order_date', 'pickup_time', 'created_at', 'updated_at', 'items', 'items_data']

    def create(self, validated_data):
        items_data = validated_data.pop('items_data', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            menu_item_id = item_data.get('menu_item_id')
            quantity = item_data.get('quantity')
            subtotal = item_data.get('subtotal')
            OrderItem.objects.create(
                order=order,
                menu_item_id=menu_item_id,
                quantity=quantity,
                subtotal=subtotal
            )
        return order

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

