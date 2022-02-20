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
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count


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

        get_date = request.GET.get("date")

        if not get_date:
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            get_date = datetime.datetime.strftime(yesterday, "%m/%d/%Y")  # type: ignore

        my_date = datetime.datetime.strptime(get_date, "%m/%d/%Y").date()

        queryset = News.objects.filter(postDate=str(my_date))
        qs = (
            News.objects.annotate(month=TruncMonth("postDate"))
            .values("month")
            .annotate(count=Count("title"))
        ).order_by("-month")
        days = [
            {
                "date": x["month"].strftime("%B %Y"),
                "date_link": x["month"].strftime("%m/01/%Y"),
                "count": x["count"],
            }
            for x in qs
        ]
        try:
            earliest = News.objects.all().earliest("postDate")
            latest = News.objects.all().latest("postDate")
            e = earliest.postDate.strftime("%m/%d/%Y")
            l = latest.postDate.strftime("%m/%d/%Y")
        except:
            e = None
            l = None


        return render(
            request,
            self.template_name,
            {
                "news": queryset or None,
                "days": days,
                "earliest": e,
                "latest": l,
                "yesterday": get_date,
            },
        )


class PostView(View):
    """
    Now it is render template test blog like
    Needs to split to two separate functions
    """

    template_name = "blog_post.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        qs = (
            News.objects.annotate(month=TruncMonth("postDate"))
            .values("month")
            .annotate(count=Count("title"))
        )
        days = [
            {
                "date": x["month"].strftime("%B %Y"),
                "date_link": x["month"].strftime("%m/01/%Y"),
                "count": x["count"],
            }
            for x in qs
        ]
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        get_date = datetime.datetime.strftime(yesterday, "%m/%d/%Y")  # type: ignore

        post = News.objects.get(newsId=pk)
        return render(
            request,
            self.template_name,
            {"post": post, "days": days, "yesterday": get_date},
        )
