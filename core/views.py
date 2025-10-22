from django.shortcuts import render
from .models import User, MenuItem, Order, OrderItem, Payment, Notification, Inventory, Tag
from .serializers import UserSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer, NotificationSerializer, InventorySerializer, TagSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Get current authenticated user
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class MenuItemViewset(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        """
        Allow anyone to view menu items.
        Only staff and admin can create, update, or delete.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes_list = [permissions.AllowAny]
        else:
            # Import the custom permissions
            from .permissions import IsAdminOrStaff
            permission_classes_list = [IsAdminOrStaff]
        return [permission() for permission in permission_classes_list]

class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Return orders specific to the logged-in user.
        Staff/admin users can see all orders.
        """
        user = self.request.user
        
        # Staff and admin can access ALL orders (for both list and detail views)
        if user.role in ['staff', 'admin']:
            return Order.objects.all().order_by('-created_at')
        
        # Regular users can only see their own orders
        return Order.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Automatically attach the logged-in user when creating a new order.
        """
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        """
        Allow users to cancel (update status) of their own orders.
        Staff can update any order.
        """
        instance = self.get_object()

        # Check if user is staff/admin OR is the order owner
        is_staff = request.user.role in ['staff', 'admin']
        is_owner = instance.user == request.user
        
        if not is_staff and not is_owner:
            return Response(
                {"error": "You are not authorized to modify this order."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Use the serializer to update the instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InventoryViewset(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view tags
