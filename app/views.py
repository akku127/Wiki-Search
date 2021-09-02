from django.shortcuts import render
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
import requests
from bs4 import BeautifulSoup


# Create your views here.

def index(request):
    num = None
    topic = ""
    pages = []
    pics = []

    topic_suggestion = None
    if request.GET.get("topic"):
        topic = request.GET.get("topic")
        num = request.GET.get("results")
        # wikipedia suggestions disabled for now as sometimes doesnt give desired results for eg if we search for cat the .suggest suggests hat.

        if wikipedia.suggest(topic):
            topic_suggestion = wikipedia.suggest(topic)
        # else:
        #     print("entered else statement")
        #     topic_suggestion = topic

        # topic_suggestion = topic
        search_topics = wikipedia.search(topic, results=num)
        # print(search_topics)
        for item in search_topics:
            try:
                page = wikipedia.page(item, auto_suggest=False)
                pages.append(page)
                wikipage = requests.get(page.url)
                soup = BeautifulSoup(wikipage.content, "html.parser")
                try:
                    pic = "https:" + soup.find("td", class_="infobox-image").find("a", class_="image").img['src']
                except:
                    pic = ""
                print(page.title)
                pics.append(pic)
            except PageError as e:
                print("Exception_________________error", e)
                # print("Except block")
                print(item)
            except DisambiguationError as e:
                print("Disambiguation__________________ error")
                print(e)
    return render(request, 'app/index.html',
                  {'pages': zip(pages, pics), 'suggestion': topic_suggestion, 'topic': topic, 'num': num})
