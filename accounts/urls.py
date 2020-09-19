from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    # path('home/', views.home),
    path('d2b/', views.d2b,name='d2b'),
    path('askintent/<str:pk>',views.askintent ,name='askintent')
]
