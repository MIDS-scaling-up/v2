# Labs 5: Simple models with TF2

## a. Layers and training
This sequence of simple labs builds upon the beginner TF2 lab:
1. Please make sure you have your `w251/tensorflow:nx-dp4.4` container up and running with Jupyter and that you have browser access to it.  Please refer to the homework instructions if you already shut it down and need to restart it.
1. Let us run the training again -- this time, let us set batch size to 128 and make sure we use the test split as the validation parameter during training
1. Lets use matplotlib and display one of the images from the test set (e.g. sample 2).  Does it get correctly classified by your trained model?
1. Please borrow the model structure from [here](https://github.com/dragen1860/TensorFlow-2.x-Tutorials/tree/master/01-TF2.0-Overview) and try it here.  Does it help improve validation accuracy?
1. So far, we have been using the Keras Sequential API.  However, the [Functional API](https://keras.io/guides/functional_api/) is far more powerful. Keeping the structure of the model the same, please use the sequential API to describe the model and train it.
1. Now, let us build a two path hybrid model that uses both architectures and converges just before the final fully connected layer. Hint: use the `tf.keras.layers.concatenate` layer. Train it. Does it improve accuracy?

## b. Simple Generative Adversarial Networks
This example builds on the [TensorFlow DCGAN](https://www.tensorflow.org/tutorials/generative/dcgan) tutorial
1. Download the notebook and upload it to your NX
1. At the top, replace pip with pip3. You will also need to `!apt update && apt install -y git` to get through the software installation step
