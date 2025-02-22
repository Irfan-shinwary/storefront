from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register('products',views.ProductViewSet, basename='products')
router.register('collections',views.CollectionViewSet)
router.urls

products_router =routers.NestedDefaultRouter(router,'products', lookup='product')
products_router.register('reviews',views.ReviewVieSet, basename='product-reviews')


urlpatterns=[
    path('',include(router.urls)),
    path('',include(products_router.urls)),

    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetails.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetails.as_view(), name='collection-detail')

]