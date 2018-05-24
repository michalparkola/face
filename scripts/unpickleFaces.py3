#!/usr/bin/python3

import os
import pickle

def loadKnownFaces(knownFacesPickle):
    fp = open(knownFacesPickle, "rb")
    knownFaces = pickle.load(fp, encoding='latin1')
    fp.close()
    return knownFaces

knownFaces = loadKnownFaces("../data/knownFaces.pickle")
print(knownFaces)
