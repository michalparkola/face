import os
import cv2
import numpy as np
np.set_printoptions(precision = 2)
import openface
import pickle

fileDir = "/root/openface/"
modelDir = os.path.join(fileDir, 'models')
openfaceModelDir = os.path.join(modelDir, 'openface')

dlibModelDir = os.path.join(modelDir, 'dlib')
dlibFacePredictor = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
align = openface.AlignDlib(dlibFacePredictor)

networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
imgDim = 96
net = openface.TorchNeuralNet(networkModel, imgDim)

def dataURItoCV2img(dataUri):
    ar = np.fromstring(dataUri.decode('base64'), np.uint8)
    img = cv2.imdecode(ar, cv2.IMREAD_COLOR)
    return img

def findAndAlignFace(rgbImg):
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))
    alignedFace = align.align(imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))
    return alignedFace

def getRep(imgPath):
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    alignedFace = findAndAlignFace(rgbImg)
    rep = net.forward(alignedFace)
    return rep

def loadKnownFaces(knownFacesPickle):
    fp = open(knownFacesPickle, "r")
    knownFaces = pickle.load(fp)
    fp.close()
    return knownFaces

def getRepForDataURI(dataUri):
    bgrImg = dataURItoCV2img(dataUri)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    alignedFace = findAndAlignFace(rgbImg)
    rep = net.forward(alignedFace)
    print("getRepForDataURI:" + str(rep))
    return rep

def whoIsThis(whoIsThisRep, knownFaces):
    distances = {}
    for isThisHer in knownFaces:
        isThisHerRep = knownFaces[isThisHer][1]
        d = isThisHerRep - whoIsThisRep
        l2distance = np.dot(d, d)
        print("Comparing with {}, distance = {:0.3f}".format(isThisHer, l2distance))
        distances[isThisHer] = l2distance
    probablyHer = min(distances, key=distances.get)
    return(probablyHer, distances)