from flask import Flask, render_template, url_for, request, redirect, session
#import firebase_admin
#from firebase_admin import credentials, firestore
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management


from fellowships import fellowships
app.register_blueprint(fellowships)

from analysis import generate_umap_feature_plot

#if not firebase_admin._apps:
#    cred = credentials.Certificate('resume-68c39-firebase-adminsdk-le5uz-01999bf06d.json')
#    firebase_admin.initialize_app(cred)
#db = firestore.client()

@app.route('/submit', methods=['POST'])
def submit():
    session['data'] = generate_umap_feature_plot(gene = request.form['gene'])
    return redirect(url_for('form'))

@app.route("/form")
def form():
    data = session.pop('data', None) 
    unique_id = int(time.time())
    return render_template('/analysis/index.html', image_url=data, unique_id=unique_id)


@app.route("/")
def home():
    name = 'ya_boi'
    nav_col_left = 'nav_col_left'
    return render_template('index.html', name=name, nav_col_left=nav_col_left)

@app.route("/about")
def about():
    #users_ref = db.collection("Education")
    #docs = users_ref.stream()
    return render_template('pages/about.html')


@app.route("/vitae")
def vitae():
    return render_template('pages/vitae.html')

@app.route("/writing")
def writing():
    return render_template('pages/writing.html')

@app.route("/projects")
def projects():
    return render_template('pages/projects.html')

@app.route("/stuff")
def stuff():
    return render_template('pages/stuff.html')

@app.route("/contact")
def contact():
    return render_template('pages/contact.html')

