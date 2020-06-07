#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Frameworks 
Closely follows : 
    https://keras.io/api/applications/
    https://github.com/rwightman/pytorch-image-models
    
If you miss packages :
    pip install opencv-python
    pip install scikit-image
    pip install tensorflow
    pip install torch torchvision
    pip install timm
    pip install Pillow==2.2.1
    pip install albumentations
"""

# 
import os
from PIL import Image
import cv2
from skimage import io
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import pandas as pd
import torch
import timm

# We use skimage to read straight from a URL 
# If you have a local image, use `img = cv2.imread('/mypath/myimage.jg')`
ELEPHANT_URL = 'http://animalia.bio/uploads/animals/photos/full/1.25x1/SPw5o18o0MDnboaFVn9a.jpg'
img = io.imread(ELEPHANT_URL)
img = cv2.resize(img, (224,224))

Image.fromarray(img)
print(f'Image shape : {img.shape}')
print(f'Image type : {img.dtype}')

# Lets make a histogram of the values
pd.Series(img.flatten()).hist(bins = 255)

'''
KERAS
'''
# Lets use imagenet trained weights to predict it
model = VGG16(weights='imagenet')
model.summary()

# Lets look at the weights behind
dir(model)
model.get_weights()[2]
model.get_weights()[2].shape

# Why are the weights this shape
for layer in model.layers:
    print(f'{layer.name}\t\t{layer.trainable}')
    

for t, layer in enumerate(model.layers):
    if t<10:
        layer.trainable = False

for layer in model.layers:
    print(f'{layer.name}\t\t{layer.trainable}')
    

# Lets process the input
x = image.img_to_array(img)
print(f'Image shape : {x.shape}; type : {x.dtype} ')
x

x = np.expand_dims(x, axis=0)
print(f'Expanded dimension shape : {x.shape}; type : {x.dtype} ')
x

x = preprocess_input(x)
print(f'Expanded dimension shape : {x.shape}; type : {x.dtype} ')
x

# Now lets use the model to predict
preds = model.predict(x)
print(f'Predictions shape : {preds.shape}; type : {preds.dtype} ')
np.argsort(preds.flatten())[::-1][:5]
#  array([101, 385, 386, 347, 343])
# https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a
print('Predicted:', decode_predictions(preds, top=3)[0])

# Lets try to extract the features from and intermediate layer.
from tensorflow.keras.models import Model
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('block4_pool').output)
block4_pool_features = model.predict(x)

block4_pool_features.shape


'''
Torch
'''
import albumentations as A
from albumentations.pytorch import ToTensor

ELEPHANT_URL = 'http://animalia.bio/uploads/animals/photos/full/1.25x1/SPw5o18o0MDnboaFVn9a.jpg'
img = io.imread(ELEPHANT_URL)
img = cv2.resize(img, (224,224))

# Augmentation : http://man.hubwiz.com/docset/torchvision.docset/Contents/Resources/Documents/transforms.html
trn_transforms = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        #A.Transpose(p=0.5),
        #A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=30, 
        #                   border_mode=cv2.BORDER_CONSTANT, value=[255,255,255], p=0.8),
        #A.GridDistortion(p=0.5),
        #A.RandomBrightnessContrast(p=0.5),
        #A.RandomCrop(int(options.tilesize*1.5), 
        #             int(options.tilesize*1.5), 
        #             always_apply=True, p=1.0),
    ])

mean_img = [0.485, 0.456, 0.406]
std_img = [0.229, 0.224, 0.225]
transform_norm = A.Compose([
    A.Normalize(mean=mean_img, std=std_img, max_pixel_value=255.0, p=1.0),
    ToTensor()
    ])

Image.fromarray(trn_transforms(image = img)['image'])

# Lets load a model
model = timm.create_model('mixnet_l', pretrained=True)
# Downloads to /Users/dhanley/.cache/torch/checkpoints/mixnet_xl_ra-aac3c00c.pth
# Normalise the image
x = transform_norm(image = img)['image']
x.shape
type(x)
x[:10,:10,0]

pd.Series(x.flatten()).hist(bins = 100)

# Predict
preds = model(x)

x.shape
x = x.unsqueeze(0)
x.shape

preds = model(x)

preds.flatten().argsort()[:5]

# lets look at the model
model

model.conv_head

model.conv_head.weight

# How do we freeze weights
model.eval()
for parameter in model.parameters():
    print(f'{parameter.shape}\t\t\t\t\tTrainable {parameter.requires_grad}')
model

# Change the number of output classes
model.classifier = torch.nn.Linear(1536, 5)

out = model(x)
out.shape
out

dir(model)

# Make the conv_stem kernel_size 1 and stride 1
model.conv_stem

model.conv_stem.kernel_size = (1,1)
model.conv_stem.stride= (1,1)

out = model(x)
out