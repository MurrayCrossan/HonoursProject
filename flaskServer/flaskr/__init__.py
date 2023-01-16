import os
from flask import Flask, request, render_template
from flask_cors import CORS
import pickle
from featureExtraction import url_to_features, generate_brandlist


def create_app(test_config=None):
    #Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        #Load the instance config, if it already exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exits
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Create the model from the pickle file and generate the brandlist.
    model = pickle.load(open(r"..\pickledModels\RF_DatasetA.sav", "rb"))
    brandlist = generate_brandlist()
    print("Model Trained")  
    CORS(app)

    #A simple page that says hello
    @app.route("/url")
    def predict_URL():
        #The visited URL is saved as a query. This query is saved to the visited_URL variable
        visited_URL = request.args.get('url')
    

        #Checks if the given url is the newtab name for chrome, returns instantly if this is the case. Saves on processing time & power.
        if visited_URL == "chrome://newtab/":
            print("Newtab is Legitimate")
            return render_template('index.html', phish_or_legit="Legitimate", website=visited_URL)

        #Sends visited_URL to the feature extraction function. Saves the extracted feature data to the features variable
        features = url_to_features(visited_URL, brandlist)
        #Makes a prediction on the given features using the model defined earlier
        prediction = model.predict([features])
        #Initializsing empty variable to be used later
        phishing_or_legitimate = ""
        

        #Statement which checks if prediciton is phishing or legitimate. Updates phishing_or_legitimate.
        if prediction == [1]:
            phishing_or_legitimate = "Phishing"
        elif prediction == [0]:
            phishing_or_legitimate = "Legitimate"

        #Updates the returned HTML file with the class predictied and the website visited. This information will be parsed by the client side app and displayed to the User if the class is phishing
        rendered_file = render_template('index.html', phish_or_legit=phishing_or_legitimate, website=visited_URL)

        #Prints the prediction to the console. Used for debugging and monitoring while the server is live.
        print("You have visited the page: {url}. It is predicited to be {pred}".format(url=visited_URL, pred=phishing_or_legitimate))
        
        #Returns the index.html file updated with the visited url and predicted class to the original get request.
        return rendered_file

    return app