from flask import Flask, url_for, render_template, request
from base64 import b64encode
import os
import pickle
from FaceEmbedding import getRepForDataURI, whoIsThis, loadKnownFaces

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template('webcam.html')

@app.route("/faces")
def allKnownFaces():
    knownFaces = loadKnownFaces("./data/knownFaces.pickle")
    return render_template('knownFaces.html', knownFaces = knownFaces)

@app.route("/recognize", methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        knownFaces = loadKnownFaces("./data/knownFaces.pickle")
        dataUri = request.form['webcam_pic']
        whoIsThisRep = getRepForDataURI(dataUri)
        probablyThis, distances = whoIsThis(whoIsThisRep, knownFaces)
        # find face, crop and calculate a representation for the captured pic
        # compare new encoding to all encodings stored in knownFaces.pickle
        return render_template('recognize.html', pic=dataUri, faces=knownFaces, who=whoIsThisRep, probably=probablyThis, distances=distances)
    else:
        return allKnownFaces()

if __name__ == "__main__":
    app.run()
