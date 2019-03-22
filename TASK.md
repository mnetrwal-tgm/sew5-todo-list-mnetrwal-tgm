# "Restful ToDo-List" - Taskdescription

## Einführung
Diese Übung gibt eine Einführung in die Verwendung von Restful-Services.

## Ziele
Das Verständnis von zustandslosen Verbindungen um Daten leicht administrieren und verteilen zu können.

## Voraussetzungen
* Grundverständnis von Python und JavaScript
* Lesen und Umsetzen von APIs
* Erstellung von Netzwerkverbindungen
* Automatisiertes Testen mittels Unit- und System-Tests

## Detailierte Ausgabenbeschreibung
### Backend
Implementieren Sie eine einfache Todo-Liste, welche ein Erstellen, das Ausgeben, Updaten und Löschen über eine ReST-Schnittstelle ermöglicht. Verwenden Sie dazu eine einfache JSON-Struktur (z.B.: {id:1, name:"Testvorbereitung abschliessen"; description:"Notwendige Informationen sammeln und mit Codebeispielen ausprobieren"}). Die einzelnen Todos sollen nach dem Beenden des Server-Dienstes persistent gespeichert werden.  

### Frontend
Entwickeln Sie eine Weboberfläche, um die Funktionen Ihres Backends nutzen zu können. Verwenden Sie dabei ein JS-Framework (Vue.js) und implementieren Sie ein intuitives User-Interface.

### Testing
Überprüfen Sie die CRUD-Funktionen mittels Unit- und System-Tests am Backend (z.B. Pytest). Vergessen Sie nicht mögliche Fehlerklassen und überprüfen Sie auch Falsch-Eingaben. Die End-To-End-Tests sollen mit einem gängigen Framework (z.B. Cypress.io) implementiert werden.  
Erstellen Sie einen Test- und einen Coveragereport für beide Teile der Implementierungen.

### Deployment
Das Testen und Deployment soll mittels einem Continous-Integration Tool durchgeführt werden. Vergessen Sie dabei nicht die Abhängigkeiten, welche durch die Trennung in Backend und Frontend entstehen. Verwenden Sie dabei gängige Tools zum lokalen Deployment (tox, venv, npm, etc.).

## Quellen
* [Flask ReST](https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example)
* [Sqlite with Python](https://docs.python.org/3/library/sqlite3.html)
* [pytest-flask Feature Reference](https://pytest-flask.readthedocs.io/en/latest/features.html)
* [Flask test_client](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.test_client)
* [Testing Flask Applications](http://flask.pocoo.org/docs/1.0/testing/#testing)
* [Vue.js Guide](https://vuejs.org/v2/guide/)
* [Cypress.io](https://www.cypress.io/)

