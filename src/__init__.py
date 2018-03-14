from flask import Flask

app = Flask(__name__)

app.secret_key = 'some_random_key'

from src.views import app