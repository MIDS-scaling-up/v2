# Homework 13: Nvidia Transfer Learning Toolkit (TLT)

The TLT is a convenience framework that's supposed to help speed up the development of custom DL video applications. Get up to speed on the TLT by going through the links below:

* https://developer.nvidia.com/transfer-learning-toolkit
* https://devblogs.nvidia.com/accelerating-video-analytics-tlt/
* https://devblogs.nvidia.com/transfer-learning-toolkit-pruning-intelligent-video-analytics/
* The [Getting Started Guide](https://github.com/MIDS-scaling-up/v2/blob/master/week13/hw/Transfer-Learning-Toolkit-Getting-Started-Guide-IVAOpenBeta.pdf) (also available in the authenticated area of the developer Nvidia portal)

Note its model pruning capabilities.  
At the moment, the TLT is still early release, and you need to apply for access. 
We have contacted Nvidia and passed on your email addresses with which you registered for the class - with the idea that you could use the same email address to register for the NGC and then get access to the TLT.  

You will need a virtual machine with a GPU.  Please obtain and set up one (including docker and nvidia docker) in Softlayer as per instructions in earlier homeworks.
Once that is done, log into the NGC with your credentials and pull the latest TLT container, e.g.
```
docker login
# make sure you enter the credentials that allow you access to the TLT
docker pull nvcr.io/nvtltea/iva/tlt-streamanalytics:v0.3_py2
```
Assuming this completed ok, you should now be able to run the TLT container. You will need to have a mountpoint or disk with some space available (let's say, 20G) - in the example below, /data is my mountpoint , and pass it through to the container.  Notice that we are also setting up a port passthrough:
```
nvidia-docker run --rm -v /data:/data -p 9888:8888 -it  nvcr.io/nvtltea/iva/tlt-streamanalytics:v0.3_py2 /bin/bash
```
Validate that your TLT command line is working by trying to list the available models:
```
root@34eda020fe6a:/workspace# tlt-pull -k $YOUR_KEY  --list_models -o nvtltea -t iva
# the output should look like this:
+-----------------------------------+-------------+----------------+----------------+-----------+-----------+-------------------------+
| Name                              | Org/Team    | Latest Version | Application    | Framework | Precision | Last Modified           |
+-----------------------------------+-------------+----------------+----------------+-----------+-----------+-------------------------+
| tlt_iva_classification_alexnet    | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-01 20:41:41 UTC |
| tlt_iva_classification_googlenet  | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-02 00:08:48 UTC |
| tlt_iva_classification_resnet18   | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-01 23:56:49 UTC |
| tlt_iva_classification_resnet50   | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-01 23:52:58 UTC |
| tlt_iva_classification_vgg16      | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-02 00:03:52 UTC |
| tlt_iva_classification_vgg19      | nvtltea/iva | 1              | Classification | TLT       | FP32      | 2019-03-02 00:06:36 UTC |
| tlt_iva_object_detection_googlene | nvtltea/iva | 1              | Detection      | TLT       | FP32      | 2019-03-02 00:48:15 UTC |
| t                                 |             |                |                |           |           |                         |
| tlt_iva_object_detection_resnet10 | nvtltea/iva | 1              | Detection      | TLT       | FP32      | 2019-03-02 00:45:16 UTC |
| tlt_iva_object_detection_resnet18 | nvtltea/iva | 1              | Detection      | TLT       | FP32      | 2019-03-02 00:37:46 UTC |
| tlt_iva_object_detection_vgg16    | nvtltea/iva | 1              | Detection      | TLT       | FP32      | 2019-03-02 00:41:00 UTC |
+-----------------------------------+-------------+----------------+----------------+-----------+-----------+-------------------------+
root@34eda020fe6a:/workspace# 
```
Now, let's go through the object detection sample:
```
jupyter notebook --ip 0.0.0.0 --allow-root
```
Point your browser to http://ip_of_your_vm:9888 and use the token that was printed to standard output when you launched your notebook.
Now, navigate to examples, detection.ipynb and follow the instructions to complete it.



