# Homework 6: The TPUs (and BERT!) IS BEING REVISED AND WILL BE RELEASED SHORTLY.  SUMMER 2019 STUDENTS PLEASE HOLD OFF STARTING IT

* Read the Google Cloud Product Overview on the [TPUs](https://cloud.google.com/tpu/)
* Read the primer on [Bert](https://github.com/google-research/bert)
* Run through the [Finetuning BERT on Google Colab](https://colab.research.google.com/github/tensorflow/tpu/blob/master/tools/colab/bert_finetuning_with_cloud_tpus.ipynb) example. Make sure to read through the code.  Is the computation time sensitive to the batch size?

* Use the pre-trained BERT model to generate embeddings for the following sentence pairs:
```
# pair 1
# i quit smoking.  how do i go about removing the tobacco premium?
# I was wondering if you can tell me how I can remove the tobacco user surcharge from my coverage plan since I am not a tobacco user

# pair 2
# how frequently is an annual checkup is covered?
# I want to know if general health checkup is covered in my insurance plan?

# pair 3
# are breast pumps covered under my plan?
# I was wondering where I can find info on breast pumps and how to get one that's covered by my insurance.
```
Calculate a simililarity metric between the pairs based on the BERT embeddings.  Are these sentences close to each other?
