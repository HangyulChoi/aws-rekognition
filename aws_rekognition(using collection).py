#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 14:59:27 2020

@author: hangyulchoi
"""

#%%  
# Creating a collection

import boto3

def create_collection(collection_id): # collection_id == name of collection
    
    client = boto3.client('rekognition')
    
    #Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId = collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done')
    
def main():
    collection_id = 'test_collection'
    create_collection(collection_id)

if __name__ == "__main__":
    main()


#%%
# Deleting a collection
    
import boto3
from botocore.exceptions import ClientError


def delete_collection(collection_id):
    
    print('Attempting to delete collection ' + collection_id)
    client=boto3.client('rekognition')
    status_code=0
    try:
        response=client.delete_collection(CollectionId=collection_id)
        status_code=response['StatusCode']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        status_code=e.response['ResponseMetadata']['HTTPStatusCode']
    return(status_code)

def main():
    collection_id='Collection'
    status_code=delete_collection(collection_id)
    print('Status code: ' + str(status_code))

if __name__ == "__main__":
    main()
    

#%%
# Adding faces to a collection

import boto3

def add_faces_to_collection(bucket, photo, collection_id):
    
    client = boto3.client('rekognition')
    
    response = client.index_faces(CollectionId = collection_id,
                                  Image = {'S3Object':{'Bucket':bucket, 'Name':photo}},
                                  ExternalImageId = photo,
                                  MaxFaces = 1,
                                  QualityFilter = "AUTO",
                                  DetectionAttributes = ['ALL'])
    
    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print(' Face ID: ' + faceRecord['Face']['FaceId'])
        print(' Location: {}'.format(faceRecord['Face']['BoundingBox']))
    
    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('  ' + reason)
    return len(response['FaceRecords'])

def main():
    
    bucket = 'hangyul-face-recognition'
    collection_id = 'test_collection'
    photo = '861.png'
    
    indexed_faces_count = add_faces_to_collection(bucket, photo, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))

if __name__ == "__main__":
    main()



#%%
import pathlib

def normalise(p):
    return str(pathlib.PosixPath(p).resolve(strict=False)).encode().decode()    
    
    
def is_normalised(path):
    return path == normalise(path)

is_normalised('kdw_M_E/glass_f_cap_f/20200317_165545.png')
normalise('kdw_M_E/glass_f_cap_f/20200317_165545.png')

#%%
# Searching for a face using an image
    
import boto3

def search_faces_by_image():
    
    collectionId='test_collection'
    bucket = 'hangyul-face-recognition'
    fileName = 'salesio-ms_201127_123610_0_L_A_GB-20111205_Facefile.png'
    threshold = 70
    maxFaces = 3
    
    client = boto3.client('rekognition')
    response = client.search_faces_by_image(CollectionId = collectionId,
                                            Image = {'S3Object': {'Bucket': bucket, 'Name': fileName}},
                                            FaceMatchThreshold = threshold,
                                            MaxFaces = maxFaces)
    
    faceMatches = response['FaceMatches']
    print('\n--Matching faces--')
    for match in faceMatches:
        print('FaceId:' + match['Face']['FaceId'])
        print('FileName: ' + match['Face']['ExternalImageId'])
        print('Similarity: ' + '{:.2f}'.format(match['Similarity']) + '%')
        
        # must print name of the person
    print('\n--Done--')   

search_faces_by_image()


#%%
# Searching for a face using its face ID

import boto3
def search_face_in_collection(face_id,collection_id):
    threshold = 90
    max_faces = 2
    client=boto3.client('rekognition')
    
    response=client.search_faces(CollectionId=collection_id,
                                 FaceId=face_id,
                                 FaceMatchThreshold=threshold,
                                 MaxFaces=max_faces)
    
    face_matches=response['FaceMatches']
    print ('--Matching faces--')
    for match in face_matches:
        print ('FaceId:' + match['Face']['FaceId'])
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
    return len(face_matches)

def main():
    
    face_id='664f9e9d-3afc-43bf-a73d-6f0cb379849d'
    collection_id='test_collection'
    
    faces=[]
    faces.append(face_id)
    
    faces_count=search_face_in_collection(face_id, collection_id)
    print("faces found: " + str(faces_count))

if __name__ == "__main__":
    main()

#%%
import boto3
IndexFaces()

#%%
# Describing a collection
    
import boto3
from botocore.exceptions import ClientError

def describe_collection(collection_id):
    
    print('Attempting to describe collection ' + collection_id)
    client=boto3.client('rekognition')
    
    try:
        response=client.describe_collection(CollectionId=collection_id)
        print("Collection Arn: " + response['CollectionARN'])
        print("Face Count: " + str(response['FaceCount']))
        print("Face Model Version: " + response['FaceModelVersion'])
        print("Timestamp: " + str(response['CreationTimestamp']))
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collection_id + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
    print('Done...')

def main():
    collection_id='test_collection'
    describe_collection(collection_id)

if __name__ == "__main__":
    main()
    




    