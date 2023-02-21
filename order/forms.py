from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'inner_container1_field', 'placeholder': 'Имя'}))
    number = forms.Field(
        widget=forms.NumberInput(attrs={'class': 'inner_container1_field', 'placeholder': 'Номер телефона c кодом'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'inner_container1_field', 'placeholder': 'Email'}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'inner_container1_field', 'placeholder': 'Адрес доставки'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'inner_container1_field', 'placeholder': 'Комментарий к заказу(необязательно)'}))
    payment = forms.ChoiceField(widget=forms.RadioSelect(),
                                choices=Order.PAYMENT_METHOD)

    class Meta:
        model = Order
        fields = ['first_name', 'number', 'email', 'address', 'comment', 'payment']

    def save(self, commit=True):
        super(OrderForm, self).save(commit=True)
        user = self.instance.initiator
        user.orders_history[str(self.instance.created)[:16]] = f'Номер заказа: {self.instance.id}'
        user.save()
        last_order = user.order_set.last()
        last_order.send_order()
        return super(OrderForm, self).save(commit=True)
