from web import create_app

# Initialize/start WSGI development server
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
