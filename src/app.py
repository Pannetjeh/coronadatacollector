
from flask import Flask, render_template, request, session, make_response, flash, redirect
from models.user import User
from common.database import Database
from models.coronadata import CoronaData
from models.statistics import read_mongo, first_graph
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)
app.secret_key = "ruben"

@app.route("/")
# The Home page of the webapplication (Home.html)
def home():
    return render_template('home.html')

@app.route("/welcome")
# The welcome page after registering or login
def welcome():
    return render_template("profile.html")

@app.route("/logout")
# After logging out clear the Cookie session and go back to homepage
def logout():
    session['email'] == None
    session.clear()
    return render_template("home.html")
    
@app.route("/auth/logout")
def logout_user():
    return render_template("home.html")

@app.route("/login")
def login_template():
    return render_template('login.html')

@app.route("/register")
def register_template():
    return render_template('register.html')

@app.before_first_request
# Before the first request of the Application initialize the MongoDatabase
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
# Get the email and password from the login.html form
def login_user():
    email = request.form['email']
    password = request.form['password']
    # Check if the username and password is valid 
    if User.login_valid(email, password):
        User.login(email)

    # If not, then return to homepage with the text that the username/password combination is incorrect
    else:
        return render_template("login.html", text = "The username/password combination is incorrect")

    return redirect('/welcome')

@app.route('/auth/register', methods=['POST', 'GET'])
def register_user():
    # When submitting for register, get the email and password from the register.html form
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        # If user already exist in the database redirect to welcome page
        if User.get_by_email("email"): 
            return render_template("register.html", text = "The username already exists")
        # If the user does not exist create the user
        else:
            User.register(email, password)
            return redirect('/')

@app.route('/coronadata/<string:user_id>')
@app.route('/coronadata')
# Needed for the coronadata response
def user_corona(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    #Corona data will be as the data. Get the corona data needs to be resolved from SQL?
    if  Database.find_one("coronadata", {"username": user.email}):
        coronadata = user.get_coronadata()
        return render_template("user_corona.html", coronadata = coronadata, email=user.email)
    else: 
        return redirect('/coronadatanew')


@app.route('/coronadatanew', methods=['POST', 'GET'])
#Page for creating and updating new corona information
def create_new_coronadata():
    # To load the page, show the fill in form
    if request.method == 'GET':
        return render_template('new_coronadata.html')
    else:
        # If the information is submitted get all the information from the form
        corona = request.form['corona']
        corona_relations = request.form['corona_relations']
        age = request.form["age"]
        gender = request.form["gender"]
        province = request.form["province"]
        user = User.get_by_email(session['email'])
        
        # Create a new coronaData object
        new_coronaData = CoronaData(user.email, corona, corona_relations, \
            age, gender, province)
        
        # Does the coronadata already exists in the database? Yes update, no create a new entry
        if Database.find_one("coronadata",  {"username": session['email']}):
            new_coronaData.update_to_mongo()
        else:
            new_coronaData.save_to_mongo()
            

        return make_response(user_corona(user._id))

# Creating the charts and graphs 
@app.route('/coronadatastats', methods=['POST', 'GET'])
def show_coronadata():
    # Get the scripts and information from Bokeh to display on the html page
    script1, div1 = components(first_graph())
    cdn_js=CDN.js_files[0]

    return render_template("statistics.html", script1=script1, div1=div1,
     cdn_js=cdn_js)

if __name__ == '__main__':
    app.debug = True
    app.run()

