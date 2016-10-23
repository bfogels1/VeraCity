from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_cors import CORS, cross_origin
import textCheck
 
app = Flask(__name__)
CORS(app)
 
@app.route("/<string:selectedText>/", methods=['GET'])
def veraCity(selectedText):
    #Insert Sam's code on selectedText

    message = textCheck.init(selectedText)
 
    return selectedText + " was tested. " + message
    #return render_template(
        #'test.html',name=name)
 
if __name__ == "__main__":
    app.run()
