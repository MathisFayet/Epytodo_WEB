##
## EPITECH PROJECT, 2020
## WEB_epytodo_2019
## File description:
## __init__
##

from flask import Flask, jsonify, request, render_template, json, session
from app.controller import *
from app.models import *

app = Flask(__name__)
app.config.from_object('config')

database = DBConnection(app)

from app import views