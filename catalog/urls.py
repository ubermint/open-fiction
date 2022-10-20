from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('book/<int:uid>/', views.book, name='book'),
    path('store/<int:sid>/', views.store, name='store'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("post_review/<int:uid>/", views.post_review, name="post_review"),
    path("del_review/<int:rid>/", views.del_review, name="del_review"),
    path("about", views.about, name="about"),
]