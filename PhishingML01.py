
from flask import Flask
from flask import render_template, redirect, request

from models import ext1
from models.decision_tree import decisionTree
from models.knn import knn
from models.lr import lr
from models.mlp import mlp
from models.Naive_bayes import naive_bayes
from models.Random_forest import RandomForest
from models.svm import svm

from models.funfunction2 import dataExtraction
from models.visualization import visual


app = Flask(__name__)

app.secret_key = "somerandomstringisrequired"

url = ""

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def homepage():


    return render_template('home.html', error="")


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        URL = request.form['URL']

        return render_template('urlfile.html', URL=URL)

    return render_template('/')

@app.route('/classifier', methods=['GET', 'POST'])
def classifier_page():

    try:
            if request.method == 'POST':
                global url
                url = request.form['URL']
                return render_template('classifiers.html', url=url  )
    except:

            error = "Invalid Url"

            return render_template('home.html',error=error)


@app.route('/classification', methods=['GET', 'POST'])
def classification_page():
    #domain = "https://www.theunitedcargo.com/195.2356.3588/india-bix//.fox"
    # url_tokenizer(domain)
    classifier_name = request.args.get('classifier_name')
    error = "hey    "
    try:

                global url

                #url = url.split("?")[0]


                feat = ext1.source_code_features(url)

                ext = ext1.featureExtraction(url)


                dataset = dataExtraction.generate_data_set(url)

                if(classifier_name=="decisionTree"):
                    output = decisionTree.load_data(dataset)
                    classifier_name = "Decision Tree"

                if(classifier_name=="lr"):
                    output = lr.load_data(dataset)
                    classifier_name = "Logistic Regression"


                if(classifier_name=="svm"):
                    output = svm.load_data(dataset)
                    classifier_name = "Support Vector Machine"

                if(classifier_name=="knn"):
                    output = knn.load_data(dataset)
                    classifier_name = "K Nearest Neighbors"

                if(classifier_name=="RandomForest"):
                    output = RandomForest.load_data(dataset)
                    classifier_name = "Random Forest"

                if(classifier_name=="mlp"):
                    output = mlp.load_data(dataset)
                    classifier_name = "Multi Layered Perceptron"

                if(classifier_name=="naive_bayes"):
                    output = naive_bayes.load_data(dataset)
                    classifier_name = "Naive Bayes"

                error = "this is error"

                isPhishing = "Legitimate"
                if(output[0]==-1):
                    isPhishing = "Phishing Website"



                return render_template('classification.html', feat=feat, ext=ext, URL=url, output=isPhishing, classifier_name=classifier_name)

    except:




            return render_template('home.html',error=error)


@app.route('/visualization')
def visualization_page():
    global url
    dataset = dataExtraction.generate_data_set(url)
    visual.pie_chart(dataset)
    visual.barGraph(dataset)
    visual.stackedGraph(dataset)
    return render_template('visualization.html', URL=url)




if __name__ == '__main__':
    app.run(port=5014, debug=True)
