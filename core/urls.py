from django.urls import include, path
from rest_framework import routers
from .views import UserViewset,MenuItemViewset, OrderItemViewset, OrderViewset, PaymentViewset, InventoryViewset, NotificationViewset, TagViewset, get_current_user

#Instance the router
router = routers.DefaultRouter()

#Register all the viewsets
router.register(r'users', UserViewset)
router.register(r'menu', MenuItemViewset)
router.register(r'order', OrderViewset, basename='order')
router.register(r'order-item', OrderItemViewset)
router.register(r'payment', PaymentViewset)
router.register(r'inventory', InventoryViewset)
router.register(r'notification', NotificationViewset)
router.register(r'tags', TagViewset)



urlpatterns = [
    path('', include(router.urls)),
    path('me/', get_current_user, name='current_user'),
]