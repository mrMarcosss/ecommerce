from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from products.forms import VariationInventoryFormSet
from products.mixins import StaffRequiredMixin
from products.models import Product, Variation, Category


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'products/product_list.html'


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        context['products'] = (product_set | default_products).distinct()
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['related'] = Product.objects.get_related(self.get_object()).order_by('?')[:7]
        return context


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return qs


class VariationListView(StaffRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VariationListView, self).get_context_data(**kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            qs = Variation.objects.filter(product=product)
        return qs

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get('pk')
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
            messages.success(request, 'Your inventory and pricing has been updated')
            return redirect('products:product_list')
