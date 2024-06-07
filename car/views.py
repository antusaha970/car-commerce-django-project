from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .models import Car, Brand
from .forms import SignUpForm, UpdateUserForm
# Create your views here.


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy("homePage")
    template_name = "authForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Sign up'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user=user)
        return response


class LogOutUserView(LogoutView):
    next_page = reverse_lazy("homePage")


class LogInUserView(LoginView):
    success_url = reverse_lazy("homePage")
    template_name = "authForm.html"
    next_page = reverse_lazy("homePage")
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login"
        return context


class UpdateUserView(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = "authForm.html"
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(TemplateView):
    template_name = "profile.html"


class HomePage(ListView):
    model = Car
    template_name = 'home.html'

    def get_queryset(self):
        q = super().get_queryset()
        brand = self.kwargs.get('brand')
        if brand is not None:
            q = Car.objects.filter(brand__id=brand)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = context['object_list']
        context['brands'] = Brand.objects.all()
        return context
