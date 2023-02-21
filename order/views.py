
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from home.models import Basket

from .forms import OrderForm


class OrderView(SuccessMessageMixin, CreateView):
    template_name = 'order/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')
    success_message = 'Ваш заказ принят'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        order_content = ''
        basket = self.request.user.basket_set.all()
        for item in basket:
            order_content += f'{str(item.product)} x {item.quantity} | '
        form.instance.content = order_content
        basket.delete()
        return super(OrderView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['total_sum'] = sum([i.summa() for i in context['baskets']])
        return context
