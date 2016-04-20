from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, ListView, DetailView
from orders.forms import AddressForm, UserAddressForm
from orders.mixins import CartOrderMixin
from orders.models import UserAddress, UserCheckout, Order
from products.mixins import LoginRequiredMixin


class OrderDetailView(DetailView):
    model = Order

    def dispatch(self, request, *args, **kwargs):
        try:
            user_check_id = self.request.session.get('user_checkout_id')
            user_checkout = UserCheckout.objects.get(id=user_check_id)
        except UserCheckout.DoesNotExist:
            user_checkout = UserCheckout.objects.get(user=request.user)
        except:
            user_checkout = None
        obj = self.get_object()
        if obj.user == user_checkout and user_checkout is not None:
            return super(OrderDetailView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()

    def get_queryset(self):
        user_check_id = self.request.user.pk
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return super(OrderListView, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = 'forms.html'
    success_url = 'order_address'

    def get_checkout_user(self):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'

    def dispatch(self, request, *args, **kwargs):
        b_address, s_address = self.get_addresses()
        if b_address.count() == 0:
            messages.success(request, 'Please add a billing address before continuing')
            return redirect('user_address_create')
        elif s_address.count() == 0:
            messages.success(request, 'Please add a shipping address before continuing')
            return redirect('user_address_create')
        else:
            return super(AddressSelectFormView, self).dispatch(request, *args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        b_address = UserAddress.objects.filter(
            user=user_checkout,
            type='billing'
        )
        s_address = UserAddress.objects.filter(
            user=self.user_checkout,
            type='shipping'
        )
        return b_address, s_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        b_address, s_address = self.get_addresses()
        form.fields['billing_address'].queryset = b_address
        form.fields['shipping_address'].queryset = s_address
        return form

    def form_valid(self, form):
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('checkout')
