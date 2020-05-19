# TFLite Image Classifier

This is based on Google Coral example https://github.com/google-coral/tflite/tree/master/python/examples/classification.  

## Running
This classifier can be run with the following:
```
python3 classify_image.py \
  --model models/mobilenet_v1_1.0_224_quant.tflite \
  --labels models/imagenet_labels.txt \
  --input images/parrot.jpg
```
To see all available options, run
```
python3 classify_image.py
```

## Models
The following models come with this lab:
- efficientnet-L_quant.tflite
- inception_v4_299_quant.tflite
- mobilenet_v1_1.0_224_quant.tflite
- mobilenet_v2_1.0_224_quant.tflite

## Label File
The following label file is included as works with all supplied models:
- imagenet_labels.txt

## Sample image
The following sample image is included:
- parrot.jpg
