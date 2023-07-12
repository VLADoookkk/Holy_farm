from django.urls import path
from .views import CategoryCreateView, ProductCreateView, CategoryListView, ProductListView, AddingAccounts

urlpatterns = [
    path('v1/categorycreate/', CategoryCreateView.as_view(), name='category-create'),
    path('v1/productcreate/', ProductCreateView.as_view(), name='product-create'),
    path('v1/categorylist/', CategoryListView.as_view(), name='category-list'),
    path('v1/productlist/', ProductListView.as_view(), name='product-list'),
    path('v1/addingaccounts/<int:pk>/', AddingAccounts.as_view(), name='adding-accounts'),
    # path('v1/updateaccountfile/', UpdateAccountFileView.as_view(), name='update-account-file'),
]