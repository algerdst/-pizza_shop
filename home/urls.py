from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('pizza/<slug:slug_name>', views.AboutProductDetailView.as_view(), name='about_product'),
    path('category/<int:category_id>/', views.ProductsListView.as_view(), name='products'),
    path('page/<int:page>/', views.ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket/remove/<int:id>/', views.basket_remove, name='basket_remove'),
]
