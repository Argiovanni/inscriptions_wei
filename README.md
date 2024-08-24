# inscriptions_wei
petite app web en django pour faciliter la gestion des inscriptions du wei

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
$ python manage.py makemigrations 
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```
