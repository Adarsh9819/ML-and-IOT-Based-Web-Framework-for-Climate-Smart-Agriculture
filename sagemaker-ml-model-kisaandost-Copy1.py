#!/usr/bin/env python
# coding: utf-8

# In[14]:


#DATA PREPARATION

import pandas as pd

#read data
data = pd.read_csv('data/crop.data', header=None)


#convert to numerical value
data[7] = data[7].replace('rice', 0)
data[7] = data[7].replace('maize', 1)
data[7] = data[7].replace('chickpea', 2)
data[7] = data[7].replace('kidneybeans', 3)
data[7] = data[7].replace('pigeonpeas', 4)
data[7] = data[7].replace('mothbeans', 5)
data[7] = data[7].replace('mungbean', 6)
data[7] = data[7].replace('blackgram', 7)
data[7] = data[7].replace('lentil', 8)
data[7] = data[7].replace('pomegranate', 9)
data[7] = data[7].replace('banana', 10)
data[7] = data[7].replace('mango', 11)
data[7] = data[7].replace('grapes', 12)
data[7] = data[7].replace('watermelon', 13)
data[7] = data[7].replace('muskmelon', 14)
data[7] = data[7].replace('apple', 15)
data[7] = data[7].replace('orange', 16)
data[7] = data[7].replace('papaya', 17)
data[7] = data[7].replace('coconut', 18)
data[7] = data[7].replace('cotton', 19)
data[7] = data[7].replace('jute', 20)
data[7] = data[7].replace('coffee', 21)


#shuffle
data = data.sample(frac=1).reset_index(drop=True)


#change label column index
data = data[[7, 0, 1, 2, 3, 4, 5, 6]]


#split(train, val sets)
train_data = data[:1800]
val_data = data[1800:]



# In[15]:


#MOVE PREPARED DATA IN CREATED S3 BUCKET

import boto3

bucket_name = 'sagemaker-build-and-deploy-model-s3-kisaandost-sagemaker'

train_data.to_csv('data.csv', header=False, index=False)
key = 'data/train/data'
url = 's3://{}/{}'.format(bucket_name, key)

# Create a session and upload the file to S3
boto3.Session().resource('s3').Bucket(bucket_name).Object(key).upload_file('data.csv')

val_data.to_csv('data.csv', header=False, index=False)
key = 'data/val/data'
url = 's3://{}/{}'.format(bucket_name, key)

# Create a session and upload the file to S3
boto3.Session().resource('s3').Bucket(bucket_name).Object(key).upload_file('data.csv')


# In[28]:


#CREATE MODEL
import sagemaker
from sagemaker import image_uris
from sagemaker import get_execution_role

bucket_name = 'sagemaker-build-and-deploy-model-s3-kisaandost-sagemaker'

# Specify the XGBoost version
xgboost_version = "1.5-1"

# Retrieve the URI of the XGBoost container with the specified version
container = image_uris.retrieve('xgboost', boto3.Session().region_name, version=xgboost_version)

key = 'model/xgb_model'
s3_output_location = 's3://{}/{}'.format(bucket_name, key)

# Creating the estimator using the new method names and parameter names
xgb_model = sagemaker.estimator.Estimator(
    container,
    get_execution_role(),
    instance_count=1,
    instance_type='ml.m4.xlarge',
    volume_size=5,
    output_path=s3_output_location,
    sagemaker_session=sagemaker.Session()
)

# Set hyperparameters as before
xgb_model.set_hyperparameters(
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    objective='multi:softmax',
    num_class=22,
    num_round=10
)



# In[29]:


#Train Model

train_data = 's3://{}/{}'.format(bucket_name, 'data/train')
val_data = 's3://{}/{}'.format(bucket_name, 'data/val')

train_channel = sagemaker.session.s3_input(train_data, content_type='text/csv')
val_channel = sagemaker.session.s3_input(val_data, content_type='text/csv')

data_channels= {'train': train_channel, 'validation': val_channel}

xgb_model.fit(inputs=data_channels)


# In[30]:


#Deploying trained model


xgb_predictor = xgb_model.deploy(initial_instance_count=1,
                                instance_type='ml.m4.xlarge')

