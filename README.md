# inscriptions_wei
petite app web en django pour faciliter la gestion des inscriptions du wei
[@author: Arthur Bongiovanni (Argiovanni)]

N.B.: Il faut créer les utilisateur manuellement : 
        soit directement en ligne de commande 
        soit depuis le menu admin (http://web_app_address:port/admin)

TODO : - il n'y a pas encore de scripts pour ajouter les bungalows dans la DB
            (une fois que la noche nous aura envoyé le plan du camping et les bungalow a disposition il seront ajouté via un script)
       - Améliorer/modifier la façon de gérer les bungalows et les cautions lié
       - ajouter un moyen de créer un compte depuis l'application
       - améliorer le visuel


Before 1st lunch
```bash
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv venv
$ source venv/bin/activate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
$
$ # create a super_user
$ python3 manage.py createsuperuser
$ # enter your username and password of choice
```

Update Database :

```bash
$ # add Inscrit objects to DB -> csv file should be obtain via the Churros's shotgun "result"
$ python3 manage.py populate_db path/to/your/csv/file.csv
$
```

Manual launch : 
```bash
$ # Start the application (development mode)
$ python3 manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

Docker launch :
make sure there is a .env file in the same directory as the Dockerfile
if not, you can create one using the env.sample file provided 
(or just an empty one if the value in site_wei/settings.py are to your liking (devellopment or local env))

```bash
$ # Start the application
$ docker-compose up --build -d
$
$ # Access the web app in browser: http://127.0.0.1:85/
```
