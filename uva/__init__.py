from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask import *
import views

app = Flask(__name__)
