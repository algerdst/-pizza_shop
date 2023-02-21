from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import ContextMixin
from home.models import Basket
from users.models import EmailVerification, User

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm


class LogoutProfileView(LogoutView):
    model = User
    template_name = 'users/logout.html'


class LoginProfileView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.request.user.id,))


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    success_message = "На ваш e-mail отправлена ссылка для верификации аккаунта, ссылка будет действительна в" \
                      " течение 48 часов"


@method_decorator(login_required, name='dispatch')
class BasketView(TemplateView):
    model = Basket
    template_name = 'users/cart.html'

    def get_context_data(self, **kwargs):
        context = super(BasketView, self).get_context_data()
        context['basket'] = Basket.objects.filter(user=self.request.user)
        context['total_sum'] = sum([i.summa() for i in context['basket']])
        context['table_tags'] = ['', 'Товар', 'Цена', 'Количество', 'Итог']
        return context


class VerifyView(ContextMixin, TemplateView):
    template_name = 'users/verify.html'
    title = ''

    def get_context_data(self, **kwargs):
        context = super(VerifyView, self).get_context_data(**kwargs)
        context['username'] = User.objects.get(email=self.kwargs['email'])
        return context

    def get(self, request, *args, **kwargs):
        code = self.kwargs['code']
        user = User.objects.get(email=self.kwargs['email'])
        email_verification = EmailVerification.objects.filter(code=code, user=user)

        if email_verification.exists() and email_verification[0].expiration >= now():
            user.is_verified = True
            user.save()
            return super(VerifyView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             auth.login(request, user)
#             return redirect('home')
#     else:
#         form = UserLoginForm()
#     data = {
#         'form': form
#     }
#     return render(request, 'users/login.html', context=data)


# @login_required
# def basket(request):
#     basket=Basket.objects.filter(user=request.user)
#     total_sum=sum([i.summa() for i in basket])
#     data={
#         'table_tags':['','Товар','Цена','Количество','Итог'],
#         'basket':basket,
#         'total_sum':total_sum
#     }
#     return render(request, 'users/cart.html', data)


# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             first_name = form.cleaned_data['username']
#             messages.success(request, f'Аккаунт с именем {first_name} создан!')
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method=='POST':
#         form=UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)
#         print(form.errors)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('profile')
#     else:
#         form=UserProfileForm(instance=request.user)
#     data={
#         'form':form
#     }
#     return render(request, 'users/profile.html',data)
