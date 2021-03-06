from flask import Flask, request, render_template

import sentiment, wegmans

import requests
import json

key = (insert wegmans subscipriton key);
app = Flask(__name__)

@app.route("/")
def main():
    print("rendering home\n")
    return render_template("index.html")


def queryAPIForRecipe(ID) -> str:
    get_url = 'https://api.wegmans.io/meals/recipes/{id}?api-version=2018-10-18'
    get_url = get_url.replace('{id}', str(ID))
    headers = {
        'Subscription-Key': key,
    }
    r = requests.get(get_url, headers=headers)
    rd = json.loads(r.text)

    toReturn = str(rd['name']) + " - " + str(rd['_links'][2]['href']).replace("[", "").replace("]", "") + " - " + str(rd['preparationTime']['min'])

    return toReturn

# Gets text from the webpage's textbox
@app.route('/sentiment')
def get_user_response():
    print("rendering response\n")
    input = request.args.get('text')
    print("outputting")
    out = queryAPIForRecipe(sentiment.getIDs(sentiment.analyzeText(input), 0)).split(" - ")

    return render_template("recipes.html", data=out[0], img=out[1], time=out[2])



@app.route('/wegmans')
def wegmans():
    return render_template("apiTesting.html")

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 4428, debug=True)





