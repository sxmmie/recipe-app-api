from django.urls import path

from . import views

# helps identify which app we're creating the url from when we use the reverse function.
app_name = 'user'

urlpatterns = [
    # user/create/
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
