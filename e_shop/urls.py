from django.conf import settings;from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from  . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/' , views.master , name='master'),
    path('',views.index , name='index'),
    path('signup',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),

    # add to cart paths

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    #contact
    path('contact_us',views.contact_page,name='contact_page'),

    path('checkout/',views.Checkout,name='checkout'),
    #your order
    path('order/',views.your_order,name='order'),

    #prod page
    path('product/' , views.product_value , name='product'),

    path('product/<str:id>',views.product_detail,name='product_detail'),

    path('search/' , views.search,name='search'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
