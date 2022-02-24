import os, requests
from multiprocessing import Pool
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
from django.conf import settings
from django import db

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
    local_filename = wget.download(url, bar=None)
    path = os.path.join(settings.BASE_DIR, 'data')
    
    shutil.copy(local_filename, f"{path}/{imgId}.jpg")
    os.remove(local_filename)
    return f"{path}/{imgId}.jpg"

def parse_pann(start, end):

    db.connections.close_all()
    ranges = date_ranges(start, end)
    k = 1 
    with progressbar.ProgressBar(max_value=(len(ranges) - 1)*50) as bar:
        for j, date_range in enumerate(ranges):
            
            url = f"https://pann.nate.com/talk/ranking/d?stdt={date_range}&page=1"
            parser = Parser(url)
            ul = parser.parse()
            for j, li in enumerate(ul.findAll('li')):
                img = None
                thumb = li.find('div', class_="thumb")
                title = li.find('dt').find('a').getText()

                link = li.find('a')['href']
                postId = link.split('/')[-1]
                count = li.find('span', class_="count").getText()
                rcm = li.find('span', class_="rcm").getText()
                postDate = datetime.datetime.strptime(date_range, '%Y%m%d')
                #txt
                txt = ''
                try:
                    txt = li.find('dd', class_="txt").find('a').getText()
                except:
                    pass


                html = get_html(f"https://pann.nate.com/talk/{postId}")


                try:            
                    obj = News.objects.get(newsId=postId)


                    obj.title= title
                    obj.excerpt=txt
                    obj.href=link
                    obj.count=count
                    obj.rcm=rcm
                    obj.postDate=postDate
                    obj.html=html


                except News.DoesNotExist:
                    obj = News(
                        newsId=postId,
                        title=title,
                        excerpt=txt,
                        href=link,
                        count=count,
                        rcm=rcm,
                        postDate=postDate,
                        html=html
                    )

                local_filename = '' 
                try:
                    img = thumb.find('img')['src']
                    local_filename = download(img, postId)
                    with open(local_filename, 'rb') as ff:
                        obj.tmb.save(f"{postId}.jpg", File(ff), save=True)
                        
                except Exception as e:
                    pass
                obj.save()
                try:
                    os.remove(local_filename)
                except Exception as e:
                    pass

                try:
                    bar.update(k)
                except:
                    pass
                k += 1
        



def parse_pann_crontab():
    """
    Function for crontab parsing
    """
    d = datetime.datetime.now().date()
    td = datetime.timedelta(days=1)
    y = d - td
    start = datetime.datetime.strftime(y, "%Y%m%d")  # type: ignore
    end = datetime.datetime.strftime(d, "%Y%m%d")  # type: ignore

    db.connections.close_all()
    ranges = date_ranges(start, end)
    k = 1 
    with progressbar.ProgressBar(max_value=(len(ranges) - 1)*50) as bar:
        for j, date_range in enumerate(ranges):
            
            url = f"https://pann.nate.com/talk/ranking/d?stdt={date_range}&page=1"
            parser = Parser(url)
            ul = parser.parse()
            for j, li in enumerate(ul.findAll('li')): #type: ignore
                img = None
                thumb = li.find('div', class_="thumb")
                title = li.find('dt').find('a').getText()

                link = li.find('a')['href']
                postId = link.split('/')[-1]
                count = li.find('span', class_="count").getText()
                rcm = li.find('span', class_="rcm").getText()
                postDate = datetime.datetime.strptime(date_range, '%Y%m%d')
                #txt
                txt = ''
                try:
                    txt = li.find('dd', class_="txt").find('a').getText()
                except:
                    pass


                html = get_html(f"https://pann.nate.com/talk/{postId}")


                try:            
                    obj = News.objects.get(newsId=postId)


                    obj.title= title
                    obj.excerpt=txt
                    obj.href=link
                    obj.count=count
                    obj.rcm=rcm
                    obj.postDate=postDate
                    obj.html=html


                except News.DoesNotExist:
                    obj = News(
                        newsId=postId,
                        title=title,
                        excerpt=txt,
                        href=link,
                        count=count,
                        rcm=rcm,
                        postDate=postDate,
                        html=html
                    )

                local_filename = '' 
                try:
                    img = thumb.find('img')['src']
                    local_filename = download(img, postId)
                    with open(local_filename, 'rb') as ff:
                        obj.tmb.save(f"{postId}.jpg", File(ff), save=True)
                        
                except Exception as e:
                    pass
                obj.save()
                try:
                    os.remove(local_filename)
                except Exception as e:
                    pass

                try:
                    bar.update(k)
                except:
                    pass
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

def date_ranges_chunks(start, end=None, chunk_size=30):
    '''
    returns range of dates from start to end in chunks
    '''
    ret_list = list()
    if not end:
        end_date = datetime.date.today()
    else:
        end_date = datetime.datetime.strptime(end, '%Y%m%d').date()
    start_date = datetime.datetime.strptime(start, '%Y%m%d').date()
    
    delta = datetime.timedelta(days=1)
    dates = []

    while start_date <= end_date:
        dates.append(start_date.strftime('%Y%m%d'))
        start_date += delta
    for i in range(0, len(dates), chunk_size):
        ret_list.append((dates[i:i + chunk_size][0], dates[i:i + chunk_size][-1]))
    return ret_list
    
def parse_multi(start, end, chunk_size):
    proc_n = 20 
    p = Pool(proc_n)
    p.starmap(parse_pann,date_ranges_chunks(start, end, chunk_size))





