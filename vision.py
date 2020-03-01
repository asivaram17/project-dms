#Detection
#TODO convert dictionaries to json
#Service key file in the environment

import io
import os

from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

pictures = []
yawn_data={}
#pictures.append('tb12.jpg')
#pictures.append('jimmyg.jpg')
pictures.append('yawning.jpg')
pictures.append('shouting.jpg')
pictures.append('yawn2.jpg')
pictures.append('shout2.jpg')
pictures.append('yawn3.jpg')
pictures.append('shout3.jpg')

def labels(path):
    warnings = []

    file_name = os.path.abspath(path)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels of ' + path + ':')
    for label in labels:
        if(label.description=='Mouth' or label.description=='Shout'):
            warnings.append(label.description)
        print(label.description)
    yawn_data[path+' labels'] = warnings


def face_detect(path):
    warnings = []

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)

    response = client.face_detection(image = image)
    faces = response.face_annotations

    likelihood_range = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE','LIKELY', 'VERY_LIKELY')


    print('Faces in ' + path + ':')
    for face in faces:
        #print('anger: {}'.format(likelihood_range[face.anger_likelihood]))
        #print('joy: {}'.format(likelihood_range[face.joy_likelihood]))
        #print('surprise: {}'.format(likelihood_range[face.surprise_likelihood]))
        prob_anger = likelihood_range[face.anger_likelihood]
        prob_joy = likelihood_range[face.joy_likelihood]
        prob_surprise = likelihood_range[face.surprise_likelihood]

        if(prob_anger=='POSSIBLE' or prob_anger=='LIKELY' or prob_anger=='VERY_LIKELY'):
            warnings.append('Anger')
    

        if(prob_joy=='POSSIBLE' or prob_joy=='LIKELY' or prob_joy=='VERY_LIKELY'):
            warnings.append('Joy')


        if(prob_surprise=='POSSIBLE' or prob_surprise=='LIKELY' or prob_surprise=='VERY_LIKELY'):
            warnings.append('Surprise')
        
    yawn_data[path+' face_detect'] = warnings
    if response.error.message:
        raise Exception('Error'.format(response.error.message))
        
#labels(pictures)
#face_detect(pictures)
for picture in pictures:
    labels(picture)
    face_detect(picture)

print(yawn_data)
#if warnings does not contain anger or surprise tell user to wake up