import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

fellowships = Blueprint('fellowships', __name__, url_prefix='/fellowships')

@fellowships.route('/')
def fellowships_home():
    name = 'ya_boi-1'
    nav_col_left = 'nav_col_left-1'
    return render_template('fellowships/index.html', name=name, nav_col_left=nav_col_left)

@fellowships.route("/generaladvice")
def generaladvice():
    return render_template('fellowships/generaladvice.html')

@fellowships.route("/summaryabstract")
def summaryabstract():
    return render_template('fellowships/summaryabstract.html')

@fellowships.route("/bibliography")
def bibliography():
    return render_template('fellowships/bibliography.html')

@fellowships.route("/institutionalletters")
def institutionalletters():
    return render_template('fellowships/institutionalletters.html')

@fellowships.route("/researchproposal")
def researchproposal():
    return render_template('fellowships/researchproposal.html')

@fellowships.route("/trainingplan")
def trainingplan():
    return render_template('fellowships/trainingplan.html')

@fellowships.route("/animalwork")
def animalwork():
    return render_template('fellowships/animalwork.html')

@fellowships.route("/rcr")
def rcr():
    return render_template('fellowships/rcr.html')

@fellowships.route("/specificaims")
def specificaims():
    return render_template('fellowships/specificaims.html')

@fellowships.route("/recletters")
def recletters():
    return render_template('fellowships/recletters.html')

@fellowships.route("/biosketch")
def biosketch():
    return render_template('fellowships/biosketch.html')

@fellowships.route("/reviewers")
def reviewers():
    return render_template('fellowships/reviewers.html')

@fellowships.route("/grants")
def grants():
    return render_template('fellowships/grants.html')

