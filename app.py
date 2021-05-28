# import necessary libraries
# from models import create_classes
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import joblib

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)



# engine = create_engine("sqlite:///db.sqlite")

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# # Save reference to the table
# Pet = Base.classes.pets

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/predict", methods=["GET", "POST"])
def send():

    # session = Session(engine)

    if request.method == "POST":
        print(request.form)
        if request.form["Cement"]:
          cement = request.form["Cement"]
        else:
          cement = 380
        if request.form["BlastFurnaceSlag"]:
          blastfurnaceslag = request.form["BlastFurnaceSlag"]
        else:
          blastfurnaceslag = 0
        if request.form["FlyAsh"]:
          flyash = request.form["FlyAsh"]
        else:
          flyash = 0
        if request.form["Water"]:
          water = request.form["Water"]
        else:
          water = 190
        if request.form["Superplasticizer"]:
          superplasticizer = request.form["Superplasticizer"]
        else:
          superplasticizer = 0
        if request.form["CoarseAggregate"]:
          coarseaggregate = request.form["CoarseAggregate"]
        else:
          coarseaggregate = 1100
        if request.form["FineAggregate"]:
          fineaggregate = request.form["FineAggregate"]
        else:
          fineaggregate = 900
        if request.form["Age"]:
          age = request.form["Age"]
        else:
          age = 28
        
        
        custinput = [[cement, blastfurnaceslag, flyash, water, superplasticizer, coarseaggregate, fineaggregate, age]]

        scaler = joblib.load("concrete2.sav")

        from sklearn.preprocessing import StandardScaler
        custinputscaled = scaler.transform(custinput)



        from tensorflow.keras.models import load_model
        model = load_model("maeConcrete.h5")

        custfinalpredict = model.predict(custinputscaled)
        print(custfinalpredict[0][0])


        predictions = round(custfinalpredict[0][0],2)

        predictionshigh = None
        predictionscommercial = None
        predictionsresidential = None
        predictionsfail = None

        if predictions > 70:
              predictionshigh = predictions
        elif predictions > 28:
              predictionscommercial = predictions
        elif predictions > 17:
              predictionsresidential = predictions
        else:
              predictionsfail = predictions
        # if predictions > 80:
        #   predictions = f'<span style= "color:green;">{predictions}</span>'
        # elif predictions >40:
        #   predictions = f'<span style= "color:yellow;">{predictions}</span>'
        # else:
        #   predictions = f'<span style= "color:red;">{predictions}</span>'


    print(predictions)
    return render_template("index.html", predictionshigh = predictionshigh, predictionsresidential = predictionsresidential, predictionscommercial = predictionscommercial, predictionsfail = predictionsfail)



@app.route("/ash")
def ash_page():

  return render_template("ash.html")

@app.route("/cement")
def cement_page():

  return render_template("cement.html")

@app.route("/coarse")
def coarse_page():

  return render_template("coarse.html")

@app.route("/concrete")
def concrete_page():

  return render_template("concrete.html")


@app.route("/correlation")
def corr_page():

  return render_template("correlation.html")

@app.route("/data")
def data_page():

  return render_template("data.html")

@app.route("/fine")
def fine_page():

  return render_template("fine.html")

@app.route("/locations")
def locations_page():

  return render_template("locations.html")

@app.route("/price")
def price_page():

  return render_template("price.html")

@app.route("/production")
def production_page():

  return render_template("production.html")


@app.route("/slag")
def slag_page():

  return render_template("slag.html")

@app.route("/strength")
def strength_page():

  return render_template("strength.html")

@app.route("/superplasticizer")
def super_page():

  return render_template("superplasticizer.html")

@app.route("/tons")
def tons_page():

  return render_template("tons.html")

@app.route("/water")
def water_page():

  return render_template("water.html")


if __name__ == "__main__":
    app.run()
