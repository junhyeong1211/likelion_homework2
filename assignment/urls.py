
from django.urls import path
from assignment import views
urlpatterns = [
    path('', views.index),
    path('create/',views.create),
    path('read/<id>/',views.read),
    path('update/<id>/',views.update),
    path('delete/',views.delete)
]
