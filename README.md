# inscriptions_wei
petite app web en django pour faciliter la gestion des inscriptions du wei

Manual launch : 
```bash
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv venv
$ source venv/bin/activate
$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
$
$ # populate database
$ python3 manage.py populate_db path/to/your/csv/file.csv
$
$ # Start the application (development mode)
$ python3 manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

Docker launch :
```bash
$
$ docker-compose up --build -d
$
$ # Access the web app in browser: http://127.0.0.1:5005/
```