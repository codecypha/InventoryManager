
from django.urls import path
from imanager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('add-category/', views.addCategory, name='addCategory'),
    path('list-category/', views.listCategory, name='listCategory'),
    path('edit-category/<str:pk>/', views.editCategory, name='editCategory'),
    path('edit-item/<str:pk>/', views.editItems, name='editItems'),    
    path('add-item/', views.addItems, name='addItems'),
    path('list-items/', views.listItems, name='listItems'),

    path('add-purchase/', views.addPurchase, name='addPurchase'),
    path('list-requests/', views.listPurchase, name='listPurchase'),
    path('add-supplier/', views.addSupplier, name='addSupplier'),
    path('list-supplier/', views.listSupplier, name='listSupplier'),
    path('add-returns/', views.addReturns, name='addReturns'),
    path('list-returns/', views.listReturns, name='listReturns'),
    path('add-sales/', views.addSales, name='addSales'),
    path('list-sales/', views.listSales, name='listSales'),
    path('search/', views.search, name='search'),
    path('export-csv/', views.exportCSV, name='exportCSV'),  
    path('sendemail/', views.sendemail, name='sendemail'),    
    path('managerapprove/', views.managerapprove, name='managerapprove'),  
    
]

