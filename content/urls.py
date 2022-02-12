from django.urls import path
from .views import BlogListView, HomePageView, PostView


urlpatterns = [
    path("blog", HomePageView.as_view(), name="home"),
    path("", BlogListView.as_view(), name="blog"),
    path("talk/<str:pk>", PostView.as_view(), name="talk"),
]
