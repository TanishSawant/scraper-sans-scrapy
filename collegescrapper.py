from flask import Flask, jsonify, current_app
from flask_apscheduler import APScheduler
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


app = Flask(__name__)
scheduler = APScheduler()
@app.route('/', methods=['GET'])
def linkScrapper():
#Add here:-
#with app.app_context():
                d = []
                url_news = "https://www.vjti.ac.in"         # link to scrape links from
                r = requests.get(url=url_news)  # , headers=headers
                soup = BeautifulSoup(r.text, "html.parser")
                customs = soup.find_all("div", {"class": "custom"})
                for custom in customs:
                        try:
                                links = custom.find_all("a")
                                for link in links:
                                        if "https" in link.get("href"):
                                                Links = link.get("href")    # adding URI to source IDs of links to get URL
                                        # print(Links)
                                                d.append(Links)
                                        else:
                                                Links = url_news + link.get("href")
                                        # print(Links)
                                                d.append(Links)
                        except Exception:
                                links = None

                d.pop(-1)  # removing last item for list which is not required
                json_dict = defaultdict(list)
                try:
                        for item in d:
                                title = item.split('/')[4]
                                try:
                                        json_dict[title].append(item)
                                #print(json_dict)
                                except Exception as e:
                                        print(e)

                except Exception as e:
                        print(e)

                return jsonify(json_dict)       # to decode JSON later in Flutter, converting obtained data to JSON


if __name__ == '__main__':
        scheduler.add_job(id='Scheduled Task', func=linkScrapper, trigger='interval', seconds=2)
        scheduler.start()
        app.run()
