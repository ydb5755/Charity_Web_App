from app import create_app
from flask import session


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)