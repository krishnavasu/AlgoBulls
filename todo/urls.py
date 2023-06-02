from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = "todo"   
router = DefaultRouter()
router.register('', views.TodoItemViewSet, basename='todo')

urlpatterns = [
    path('login/',view=views.LoginView.as_view()),
    path('register/',view=views.RegistrationView.as_view()),
    path('decode/',view=views.DecodeToke.as_view()),
    path('tags/',views.Tags.as_view({'get': 'list', 'post': 'create'})),
    path("todo/", views.TodoItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("todo/<int:pk>/", views.TodoItemViewSet.as_view({'get': 'retrieve',  'patch': 'partial_update','put': 'update', 'delete': 'destroy'})),
    # path('', include(router.urls)),
]
