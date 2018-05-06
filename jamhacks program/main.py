
#import pygame
import tensorflow as tf
from tensorflow.python.saved_model import loader_impl as f
# def callModel(imageObj):
#
#     return booleanDiag

sess=tf.Session()
PATH="C:/Users/kevin/desktop/retraining/saved"
finalExpDirectory=f._parse_saved_model(PATH)
test={"GPU"}
print(test)
modelObj=tf.saved_model.loader.load(sess, test, PATH)
#print(modelObj)
#tf graph pb construction
# tf.saved_model.loader.load(sess,)
