import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return facts[0].getText()


def get_pig_latin_url(input_text):
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"

    payload = {
        "input_text": input_text.strip()
    }

    response = requests.post(url, data=payload, allow_redirects=False)
    return response

def get_pig_latin_content(url):
    response = requests.get(url)

    return response


@app.route('/')
def home():
    response = get_pig_latin_url(get_fact())
    pig_latin_page = get_pig_latin_content(response.headers['Location'])

    return "{0} <br><br><br> <a href={1}>{1}</a>".format((str(pig_latin_page.content, 'utf-8')),
                                                      response.headers['Location'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

