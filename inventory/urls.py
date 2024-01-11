from django.urls import path
from inventory.views import add_product, viewproduct, get_brands, get_categories, get_subcategories

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('viewproduct/', viewproduct, name='viewproduct'),
    path('api/brands/<int:vendor_id>/', get_brands, name='get-brands'), 
    path('api/categories/<int:brand_id>/', get_categories, name='get-categories'),
    path('api/subcategories/<int:category_id>/', get_subcategories, name='get-subcategories'),    
]