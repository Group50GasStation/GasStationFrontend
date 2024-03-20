# GasStationFrontend

Web app built for software design, allows creation of quotes for fuel purchases.

# Starting the app


First, install necessary libraries from pip. Make sure you do this inside of a virtual env that you create inside of the cloned repository.

Activate the env, then install packages:

```
pip install flask flask-login flask-sqlalchemy flask-wtf
```

Then you can run

```
flask --debug --app __init__ run
```

To start the application. From there, navigate to http://127.0.0.1:5000/ to see the rendered webpage.

Changes made to html or css files will be hot reloaded upon a refresh in the browser.
