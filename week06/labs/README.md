# Labs 6: Bert Part II

In this week's homework, you leveraged BERT training code from a [public kaggle kernel](https://www.kaggle.com/yuval6967/toxic-bert-plain-vanila) and ran it on a P100 and a V100 card. Each of these have 16GB GPU memory. You may have seen that your model alone was 0.5GB when stored on disk - so it is quite large. Let's look at how to work around hardware constraints when running very large models.   
  
* How many parameters does Bert Base have ? How many layers does it have ?
  
* Even when we used [APEX](https://github.com/NVIDIA/apex) for mixed precision training, the max batch size we could get was 32 samples per batch. Take a look at the above notebook and see how you would simulate a 64 or 128 batch size without moving to a larger card. (Tip : look at the `accumulation`)
   
* What would you change to simulate a 128 batch size ?

* What do you need to change to incorporate the Bert Large Model?  How many layers does it have? How many parameters?

* What do you need to change in order to freeze the BERT model?
   
* Read through the discussion forum [here](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/discussion/93339), particularly the comments over the last 10 days. What would you do to improve your homework results, given the recommendations posted. Keep in mind that the participants used a different metric, so there reported scores may seem lower than what you achieved with `auc`.
