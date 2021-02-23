from django.urls import path, include, reverse_lazy
from .views import PagosApiView

urlpatterns = [
   path('pagos/', PagosApiView.as_view(), name=PagosApiView.name),
]
