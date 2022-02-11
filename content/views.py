from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView

from django.views import View
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests, csv, os
from django.conf import settings
from .models import News
import datetime


from .forms import NameForm


class HomePageView(TemplateView):
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def home(request):
    html = "<h1>Some home</h1>"
    return HttpResponse(html)


####################################################
## Parser starts here###############################
####################################################
class Parser:
    """
    Class for parshing pages on url
    """

    url = ""
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    def __init__(self, url):
        self.url = url

    def getHtml(self):
        r = requests.get(self.url, headers=self.HEADERS)
        return r.text

    def parse(self):
        html = self.getHtml()
        soup = BeautifulSoup(html, "lxml")
        div = soup.find("div", {"class": "product-single"})
        return div


class BlogListView(View):
    """
    Now it is render template test blog like
    Needs to split to two separate functions
    """

    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        date = kwargs.get("date") or yesterday.strftime("%Y%m%d")
        date = datetime.datetime.strptime(date, "%Y%m%d").date()
        queryset = News.objects.filter(postDate=date)
        return render(request, self.template_name, {"news": queryset})


class PostView(View):
    """
    Now it is render template test blog like
    Needs to split to two separate functions
    """

    template_name = "blog_post.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        post = News.objects.get(newsId=pk)
        return render(request, self.template_name, {"post": post})
