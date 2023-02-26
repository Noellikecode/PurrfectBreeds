from flask import Flask, render_template, request, jsonify

import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/try')
def index():
    return render_template('index.html')
@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/get_breed', methods=['POST'])
def get_breed():
    url = "https://cat-breed-classification-api.p.rapidapi.com/classify_img"
    imageUrl = request.json['imageUrl']
    querystring = {"url": imageUrl}
    headers = {
        "X-RapidAPI-Key": "3d5f46f2eamsh4682c22bd132313p169fbajsn0aeb8e420e13",
        "X-RapidAPI-Host": "cat-breed-classification-api.p.rapidapi.com"
    }

    response = requests.request("POST", url, headers=headers, params=querystring)
    breed = max(json.loads(response.text)["results"], key=lambda x: x["score"])["label"]    
    url1 = 'https://wiki-briefs.p.rapidapi.com/search'
    headers1 = {
        'X-RapidAPI-Key': '504c8dfe17msh098fce599aa04b7p1c889ejsn7a14b39efa43',
        'X-RapidAPI-Host': 'wiki-briefs.p.rapidapi.com'
    }
    params = {
        'q': breed,
        'topk': '3'
    }
    response = requests.get(url1, headers=headers1, params=params)
    data = response.json()
    information = data['summary'][0]
    return jsonify({'breed': breed, 'description': information})

if __name__ == '__main__':
    app.run(debug=True)
