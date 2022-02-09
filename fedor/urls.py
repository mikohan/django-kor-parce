from django.urls import path
from .views import ParserView


urlpatterns = [path("parser/", ParserView.as_view(), name="parser")]
