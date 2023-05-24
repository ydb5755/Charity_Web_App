from app import create_app, populate


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # populate()
        app.run(debug=False)


