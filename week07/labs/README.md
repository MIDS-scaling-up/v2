### Closer look at Recurrent Neural Nets (RNNs)

#### Overview and Background
We assume you know all about RNNs at this point.  If not, take the time and review them -- e.g. check out these awesome blog posts:
* http://karpathy.github.io/2015/05/21/rnn-effectiveness/
* http://colah.github.io/posts/2015-08-Understanding-LSTMs/
The goal of this lab is to learn how to make an RNN do what you want, and improve it.
We will be using a modified version of the setup from Machine Learning Mastery here: http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
In short, we are predicting the number of international airline passengers, in thousands, as a function of time.  We want to give to our
neural net a number of previous measurements, and have it predict the next step in the sequence.  The general goal of your team is to create
a network and tune it so as to minimize the loss for your validation dataset.

#### Setup of the lab
We assume that this is an exercise done in groups. Note the number of your group (group_num) and load http://169.44.201.108:8891/notebooks/lstm{group_num}.ipynb  For instance, if your 
group number is 3, you go to http://169.44.201.108:8891/notebooks/lstm3.ipynb .  Instructors will share access tokens to the notebooks.  These
are running on a server with a number of GPUs.  Docker, nvidia-docker, theano, keras, and jupyter are running on top of that.  
os.environ["CUDA_VISIBLE_DEVICES"] = "1" in cell 1 should list the number of GPU that you will be running on.  You will likely be sharing
the GPU with a few other teams -- but this lab is simple and it should not present a performance issue.

You should be able to just click through the lab and have the model generate a decent first pass at the predictions. Our goal, as stated above, however,
is to make the best model that we can.

#### What to tune
Generally, you can change the structure of your network (types of layers, numbers of layers) as well as its parameters (learning rates, batch size..)
We suggest you try the following:
* the look_back parameter (cell 7) specifies how many previous numbers the RNN looks at before making a prediction.  Does it help to increase
this number?
* In Cell 5, you'll see MinMaxScaler() applied to the inputs.  It helps sometimes to normalize inputs - but does it actually help in this case?
* Cell 11: try adjusting the learning rate.  A smaller learning rate should result in a more accurate network (at least in the local minimum
sense, but it may converge slower)
* learning_rate decay reduces the learning rate in half every time (1/decay) batches are processed.  Setting it to a non-zero value should help 
if your starting point is near a local minimum 
* number of rnn_units -- the more gives you a more complex and therefore adaptable network, but it may be harder to train and also result in 
overfitting
* activations.  relu is generally faster, but might cause an LSTM to have its gradients explode. tanh or sigmoid would be safer
* Type of RNN - try GAN vs LSTM
* batch size (cell 11) -  a larger number can reduce the training time but is also somewhat less accurate
* number of epochs (full passes over the data set) -- when do you stop?

#### 1D Convnets
Bonus question: can you look up convnets 1D and plug them in.  
Do they perform better than RNNs?

#### Auto-stopping
In cell 11, you should see a number of commented out lines related to callbacks, patience, and early stopping.  The idea here is to 
calculate validation loss at the end of each epoch pass and to stop if it no longer goes down.  Note that we are not training on the 
validation data, we are only using it to see whether the model is improving (and is generalizable)

#### What to do if we are overfitting?
Neural nets can be complex, which makes them prone to overfitting -- e.g. you'll see your validation loss is higher than your training loss.
In general, more data is really helpful-- neural nets want millions of rows!  If that is not possible, clever data augmentation schemes
would generally be a very good idea.  Assuming we have no time for it here, try making the network simpler (reduce the number of RNN units)
and or introduce a Dropout() layer immediately after the RNN layer (e.g. Dropout(0.5).   Note that this would cause your network to train slower
so make sure you have enough epochs!

Please note your validation loss and test RMSE scores -- and see how they compare to those of other groups. 


