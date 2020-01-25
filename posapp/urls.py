from django.urls import path
from .views import *
from . import *
app_name = 'posapp'



urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/',HomeView.as_view(),name = 'home'),
    path('logout/',LogoutView.as_view(),name = 'logout'),
    #supplier
    path('supplier/list/', SupplierListView.as_view(), name='supplierlist'),
    path('supplier/create/', SupplierCreateView.as_view(), name='studentcreate'),
    path('supplier/update/<int:pk>/',
         SupplierUpdateView.as_view(), name='supplierupdate'),
    path('supplier/delete/<int:pk>/',
         SupplierdeleteView.as_view(), name='supplierdelete'),
    
    #customer
    path('customer/list/', CustomerListView.as_view(), name='customerlist'),
    path('customer/create/', CustomerCreateView.as_view(), name='customercreate'),
    path('customer/update/<int:pk>/',
         CustomerUpdateView.as_view(), name='customerupdate'),
    path('customer/delete/<int:pk>/',
         CustomerdeleteView.as_view(), name='customerdelete'),
     
     #products
     path('product/list/', ProductListView.as_view(), name='productslist'),

     path('product/create/',ProductCreateView.as_view(),name = 'productcreate'),

     path('product/update/<int:pk>/',
         ProductUpdateView.as_view(), name='productupdate'),

     
     path('product/delete/<int:pk>/',
         ProductdeleteView.as_view(), name='productdelete'),
    

     #################### TODO:crud of products ##########
     #sales list
     path('sales/list/', SalesListView.as_view(), name='saleslist'),


     path('sales/create/',views.CreateInvoiceView,name = 'salescreate'),

     path('billing/order', views.orderBill, name='order'),

     path('bill/<int:pk>', views.BillGeneration, name='bill'),

     #chart js
     path('chart/',ChartView.as_view(),name='chart'),










    

    
    







]