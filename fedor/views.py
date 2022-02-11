from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests, csv, os
from django.conf import settings
from .models import Fedor


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


class ParserView(View):
    def get(self, request):

        Fedor.objects.all().delete()

        with open(os.path.join(settings.BASE_DIR, "data", "price.csv")) as file:
            """
            row[0] title
            row[3] price
            roe[6] pageUrl
            """
            reader = csv.reader(file, delimiter=";")
            i = 0
            for j, row in enumerate(reader):
                try:
                    url = row[6]
                    parser = Parser(url)
                    string = parser.parse()
                    spec = string.find("div", {"id": "specs"})  # type: ignore
                    description = spec.get_text().strip()  # type: ignore
                    img = string.find("img", {"class": "product-single__photo"})  # type: ignore
                    img["src"] = "http://www.master12volt.ru" + img["src"]  # type: ignore
                    print(img["src"])  # type: ignore
                    price = float(row[3].replace(",", "").replace("р", "").rstrip("."))
                    product = Fedor(
                        productUrl=url,
                        title=row[0],
                        imgUrl=img["src"],  # type: ignore
                        description=description,
                        price=price,
                        brand=None,
                    )
                    product.save()
                except Exception as e:
                    i += 1
                    print("Fucked up", e)
                # if j > 15:
                #     break

        # print(img["src"])  # type: ignore

        return HttpResponse(f"<h1>Parsing result {i}</h1>")


# Create your views here.
