from website import create_app, create_database

app = create_app()
app = create_database()

if __name__ == '__main__':
    app.run(debug=True)