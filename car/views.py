from django.shortcuts import render
from django.views.generic import ListView
from .models import Car, Brand
# Create your views here.


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
