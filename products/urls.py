from django.urls import path
from .views import CarListView,CarCreateView,CarDetailView,CarUpdateView,CarDeleteView
from . import views


urlpatterns=[
    path('list/',CarListView.as_view(),name='list'),
    path('create/',CarCreateView.as_view(),name='create'),
    path('detail/<int:pk>/',CarDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',CarUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',CarDeleteView.as_view(),name='delete'),

]