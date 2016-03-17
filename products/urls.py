from django.conf.urls import url
from products.views import ProductDetailView, ProductListView


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
]
