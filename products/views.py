from django.shortcuts import render
from django.views.generic import DetailView, ListView
from products.models import Product


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['variations'] = context['object'].variation_set.all()
        return context


class ProductListView(ListView):
    model = Product
