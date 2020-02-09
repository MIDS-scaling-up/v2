#!/bin/sh

IMAGE_SIZE=224

#mobileNet
#ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"

#googleNet
ARCHITECTURE="inception_v3"

#Learning Rate
#LR=0.005
#LR=0.1
LR=1.0

python3 -m scripts.retrain \
  --bottleneck_dir=tf_files/bottlenecks \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}"_LR=${LR}\
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=tf_files/flower_photos
