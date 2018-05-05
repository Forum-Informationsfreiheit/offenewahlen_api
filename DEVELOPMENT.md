### Der Development-Workflow

Um beim Entwickeln der App mitzumachen, empfiehlt es sich zuerst mal den Stand bei den [Milestones](https://github.com/OKFNat/offenewahlen-api/milestones?direction=asc&sort=due_date&state=open), [Projects](https://github.com/OKFNat/offenewahlen-api/projects) und das [Board](https://github.com/OKFNat/offenewahlen-api/milestones#boards?repos=96933110) mit den Issues anzusehen. Mit den Milestones koordinieren wir die großen Projekt-Phasen, und ist ein guter erster Startpunkt zum Verstehen des Entwicklungs-Standes. Mit den Projekten werden die Aufgabenbereiche unterteilt und das Board ermöglicht ein einfaches verwalten der Issues und ist somit die zentrale Übersicht für die Tasks.

### Selber coden

Lies zuerst den Absatz davor (Unser Workflow). Dann *forke* dieses Repo und *clone* es auf deinen Rechner um die App lokal zum Laufen bringen (siehe [Install](#install)). Dann such dir am besten ein Issue aus dem [Board](https://github.com/OKFNat/offenewahlen-api/milestones#boards?repos=96933110) und versuch es zu lösen. Wenn du Fragen hast, kannst du dich jederzeit via Email (info@offenewahlen.at) oder unter [Kontakt](http://offenewahlen.at/kontakt) melden. Nachdem du das Issue erledigt hast, musst du die Änderungen mittels Pull Request an dieses GitHub Repository hochladen.

Eine Person vom Team (vermutlich Stefan oder Christopher), werden dann den Pull Request reviewen. Wenn es Probleme gibt, werden wir dies im Pull Request kommentieren, wenn nicht werden wir *mergen*.

**Ersten Schritte**

1. Dieses Repository durchgehen.
2. Doku in [API Wiki](https://github.com/OKFNat/offenewahlen-api/wiki) durchgehen.
3. Aufgabenbereiche in [Projects](https://github.com/OKFNat/offenewahlen-api/projects) ansehen.
4. Task-Management via [Board](https://github.com/OKFNat/offenewahlen-api/milestones#boards?repos=96933110) ansehen.

### Ordner-Struktur

* `src/`
  * `offenewahlen_api/`: Hauptordner der Django-App.
  * `austria/`: Name des Django-Projektes. Wurde von uns einfach so gewählt.
    * `management/commands/`: enthält die Python-Scripts, welche man mittels `python src/manage.py` aufrufen kann.
	* `static/`: enthält die gesammelten Files des Projektes inklusive CSS, JavaScript und Bildern.
	* `templates/`: HTML templates mit Unterordnern für die Projekte.
	* `tests/`: Test-Scripts.
  * `static/`: die gesammelten Files aus allen Projekten (in unserem Fall ja nur ein Projekt). Wird von Python automatisch erstellt.
  * `migrations/`: Ordner und Inhalt werden bei einer Datenbank-Migrationen automatisch erstellt.
* `data/`: enthält die Daten von uns.
  * `setup/`: alle Daten, die für das Setup der App notwendig sind.
  * `test/`: alle Daten, die für die Tests notwendig sind.
* `venv/`: ist der Ordner für das Virtual Environment. Wird zu Beginn erstellt, siehe [Install](#install).

## SETUP

**Datenbank migrieren**

Damit die Datenbank-Variablen lokal vom Environment richtig an Python übergeben werden.
```
python src/manage.py makemigrations austria
python src/manage.py makemigrations
python src/manage.py migrate
```

**Documentation**

cd docs/
sphinx-quickstart

## DEVELOPMENT

**Datenbank migrieren**

Wenn Änderungen am Datenmodell, also an den Klassen in models.py, vorgenommen werden, müssen diese in die Datenbank migriert werden.
```bash
python src/manage.py makemigrations austria
python src/manage.py makemigrations
python src/manage.py migrate
```

## TESTING

**Tests**

```bash
pytest --doctest-modules src/austria/tests/
```

**Coverage**

```
coverage run --source=. src/manage.py test austria --noinput --settings=offenewahlen_api.setting
coverage report -m
coverage html
```

## DOCUMENTATION

```
cd docs/
sphinx-build -b html source build
sphinx-apidoc -f -o source ..
make html
```

### PACKAGING

```
python setup.py sdist
```
