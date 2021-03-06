# "Restful ToDo-List"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung

### Python-Flask

Rest kann auf zwei Weisen in Python implementiert werden, in Klassen wie im Flask Rest Beispiel oder mit Methoden wie in dieser App.
In beiden Fällen werden den Methoden und Klassen URL adressen und CRUD-Befehle zugewiesen auf die sie reagieren.

    @app.route('/todolists', methods=['GET', 'POST'])

Da man mehrere CRUD-Befehle einer Methode zuweisen können, muss diese natürlich inerhalb des Programms zwischen diesen unterscheiden können.

    if request.method == 'POST':

Da REST mit json arbeitet müssen die returns der Methoden zu Json umgewandelt werden und am besten mit Dictionaries gearbeitet werden.

    return json.dumps(TODOLISTS), status.HTTP_200_OK

Die Methoden müssen natürlich auch Variablen aus der adresszeile lesen können. Besagte Variablen sind, wie schon erwähnt, im Json format erhältlich.

    post_data = request.get_json()
    post_data.get('name') # Get the value to the key name

Damit das programm auch als Webserver läuft muss man folgende Zeilen in seinem Programm einfügen.

    # configuration
    DEBUG = True

    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app)

Diesen server muss man auch beim Programmaufruf starten.

    if __name__ == '__main__':
        app.run()


#### Imports

    from flask import Flask, request
    from flask_cors import CORS
    from flask_api import status
    import json

Statt json kann auch von flask jsonify importiert werden. Jedoch muss jedes 'json.dumps(arg)' somit durch 'jsonify(arg)' ersetzt werden.

### Single-Page-Application-with-Vue.js

Vue.js ermöglicht die erzeugung eines webbasierten GUI.

Um ein vue.js project zu starten muss man einfach folgende Commands in einem dafür gewählten Directory ausführen.

    npm install -g @vue/cli
    vue create my-get-app

Die Weboberflächen befinden sich in client/src/components.

Der router ist client/src/router/index.js und erlaubt dir den weboberflächen URL adressen zu zuweisen.

App.vue welches sich in client/src befinded ist der wrapper in dem die anderen .js dateien eigefügt werden.
Dies ist auch das file in dem man das vue.js logo entfernen kann.

Axios erlaubt vue.js die python-flask application anzusprechen.

### Deployment

Wir verwenden deployment-tools um Klartextzugriff auf unsere Apps zu vermeiden

#### Weboberfläche

    npm run build

Hiermit wird ein production build der App erzeugt welcher über einen http-server zugrifflich gemacht werden kann.

#### Flask-Server

Im Server ersetzt man folgende Zeilen:

    #app.run()
    http_server=WSGIServer(('',5000),app)
    http_server.serve_forever()

Wenn man die Weboberfläche damit verknüpfen will passt man außerdem noch folgende Zeile an:

    #app = Flask(__name__)
    app = Flask(__name__,static_folder="../../client/dist/static",template_folder="../../client/dist")

Man kann nun eine Route zu der Weboberfläche legen:

    @app.route('/')
    def index():
        return render_template('index.html')

### Testing

Um Backend Testing auszuführen einfach tox im project directory eingeben.

Frontend testing der Weboberfläche wird mittels "npx cypress open" im dafür gewählten directory gestarted.
Sowohl der Server als auch die Weboberfläche müssen hierbei natürlich laufen.

#### Travis-CI

Travis-CI ist wie der Name schon preisgibt ein Continous Integration Tool.

Um es mit dem Projekt zu verknüpfen muss man auf der [Website](travis-ci.com) das Github-Repository verknüpfen und in ihm ein '.travis.yml' erstellen.

##### [.travis.yml](.travis.yml)

In diesem File wird angegeben wie die Tests in Travis-CI ausgeführt werden hierfür muss eine Sprache wiefolgt festgelegt werden:

    language: python
    python:
        - "3.7"

Im Fall von python 3.7 und höher wird der folgende Zusatz benötigt:

    dist: xenial

 Es folgt die deklaration der Packages. Da tox verwendet wird und dies die nötigen Packages installierren wird, wird nur folgendes Package installiert

    install:
        - pip install tox-travis

Zuletzt muss angegeben werden welche commands ausgeführt werden sollen:

    script:
        - tox

#### Erstellen von Logs

Mittels pytest-html kann ein log-file erstellt werden. Hierzu wird in der tox.ini der Aufruf von pytest wiefolgt erweitert:

    pytest --html=testlogs/report.html --self-contained-html

Einen solchen Testreport findet man [hier](https://htmlpreview.github.io/?https://github.com/mnetrwal-tgm/sew5-todo-list-mnetrwal-tgm/blob/master/testlogs/report.html).

## Quellen
[Flask Rest](https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example)

[Full-stack single page application with Vue.js and Flask](https://codeburst.io/full-stack-single-page-application-with-vue-js-and-flask-b1e036315532)

[Developing a Single Page App with Flask and Vue.js](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs)

[Vue CLI 3 - Creating our Project](https://www.vuemastery.com/courses/real-world-vue-js/vue-cli/)

[Cypress webpage](https://www.cypress.io/)

[Travis CI](travis-ci.com)