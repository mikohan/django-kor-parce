import os, requests
from bs4 import BeautifulSoup
from content.models import News
from PIL import Image
import time
import shutil
import wget
from django.core.files import File
import datetime
import progressbar
import threading
from django.core.paginator import Paginator


def date_ranges(start, end=None):
    """
    returns range of dates from start to today
    """
    if not end:
        end_date = datetime.date.today()
    else:
        end_date = datetime.datetime.strptime(end, "%Y%m%d").date()
    start_date = datetime.datetime.strptime(start, "%Y%m%d").date()

    delta = datetime.timedelta(days=1)
    dates = []

    while start_date <= end_date:
        dates.append(start_date.strftime("%Y%m%d"))
        start_date += delta
    return dates


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
        div = soup.find("ul", {"class": "post_wrap"})
        return div


def get_html(url):
    """
    Function for scrapping pure html for post

    """
    parser = Parser(url)
    html = parser.getHtml()
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", class_="view-wrap")
    string = str(div)
    return string.replace(
        "/img/common/ico_mobile.gif", "https://pann.nate.com/img/common/ico_mobile.gif"
    )


def download(url, imgId):
    """
    Downloading thumbnails
    """
    local_filename = wget.download(url, bar=None)
    shutil.copy(
        local_filename,
        f"/home/manhee/Disk/Projects/Upwork/KoreanScraper/KorScrap/data/{imgId}.jpg",
    )
    return f"/home/manhee/Disk/Projects/Upwork/KoreanScraper/KorScrap/data/{imgId}.jpg"


def parse_pann(start, end):
    """
    Main parsing logic
    """
    ranges = date_ranges(start, end)
    k = 0
    with progressbar.ProgressBar(max_value=(len(ranges) - 1) * 50) as bar:
        for j, date_range in enumerate(ranges):
            url = f"https://pann.nate.com/talk/ranking/d?stdt={date_range}&page=1"
            parser = Parser(url)
            ul = parser.parse()
            for i, li in enumerate(ul.findAll("li")):  # type: ignore
                img = None
                thumb = li.find("div", class_="thumb")
                title = li.find("dt").find("a").getText()

                link = li.find("a")["href"]
                postId = link.split("/")[-1]
                count = li.find("span", class_="count").getText()
                rcm = li.find("span", class_="rcm").getText()
                postDate = datetime.datetime.strptime(date_range, "%Y%m%d")
                # txt
                try:
                    txt = li.find("dd", class_="txt").find("a").getText()
                except:
                    pass

                html = get_html(f"https://pann.nate.com/talk/{postId}")

                try:
                    obj = News.objects.get(newsId=postId)

                    obj.title = title
                    obj.excerpt = txt  # type: ignore
                    obj.href = link
                    obj.count = count
                    obj.rcm = rcm
                    obj.postDate = postDate
                    obj.html = html

                except News.DoesNotExist:
                    obj = News(
                        newsId=postId,
                        title=title,
                        excerpt=txt,  # type: ignore
                        href=link,
                        count=count,
                        rcm=rcm,
                        postDate=postDate,
                        html=html,
                    )

                try:
                    img = thumb.find("img")["src"]
                    local_filename = download(img, postId)
                    with open(local_filename, "rb") as ff:
                        obj.tmb.save(f"{postId}.jpg", File(ff), save=True)
                except Exception as e:
                    pass
                obj.save()

                bar.update(k)
                k += 1


def parse_comments(page):
    posts = page.object_list
    with progressbar.ProgressBar(max_value=posts.count()) as bar:

        for i, post in enumerate(posts):
            url = f"https://pann.nate.com/talk/{post.newsId}"
            post.html = get_html(url)
            post.save()
            bar.update(i)


def parse_single_thread(start_row=0):
    posts = News.objects.all()[start_row:]
    with progressbar.ProgressBar(max_value=posts.count()) as bar:

        for i, post in enumerate(posts):
            url = f"https://pann.nate.com/talk/{post.newsId}"
            post.html = get_html(url)
            post.save()
            bar.update(i)


def parse_multi():
    object_list = News.objects.all()
    paginator = Paginator(
        object_list, 3000
    )  # Show 10 objects per page, you can choose any other value
    num_pages = paginator.num_pages
    thread_list = []
    for num_page in range(1, num_pages):
        page = paginator.get_page(num_page)
        thread = threading.Thread(target=parse_comments, args=(page,))
        thread.start()
    for t in thread_list:
        t.join()

    print("Done")
