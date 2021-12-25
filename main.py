from website import create_app

app = create_app()

if __name__ == '__main__':
    #TODO: Remove debug mode in production
    app.run(debug=True)

