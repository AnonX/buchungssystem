# web package importieren
from web import create_app
#webserver initialisieren
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)