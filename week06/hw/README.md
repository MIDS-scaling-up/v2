# Homework 6

**Note this is a graded homework.**
 
1. Read the primer on [Bert](https://github.com/google-research/bert)  
2. Read about [amp mixed precision](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html) introduced with the latest version of `pytorch 1.6.*`.  
3. Read the Google Cloud Product Overview on the [TPUs](https://cloud.google.com/tpu/) 
4. Follow the below steps to run BERT in pytorch on the Jigsaw Toxicity classification dataset.   
  
### Instructions 
You will be training BERT in a jupyter notebook. Please read the below points before starting.    
* We will not be using docker, we will be using and AWS Deep Learning AMI which has all the tool readily available.   
* The book is set with 10K rows training and 5K rows validation - so you can test it fast in your initial development. For your final run, we would like you to train on at least 1M rows; and validate on at least 500K rows.  
* Please run it on a V100 VM (p3.2xlarge) and report run times on training 1M rows on both.
* You have 8 sections found in the jupyter notebook to complete the training of BERT and answer some questions. The first 5 seem challenging - but there is a script linked in the book which should make help a lot - should be just copy and pasting the correct code chunks.
* The Huggingface transformers code changed since the original Kaggle kernel was created.  Use the AdamW optimizer.
* We give a reference kaggle kernel where you can leverage a lot of the code. Native mixed precision was not available when that notebook was written, we would like you to port it to the new native mixed precision. We give some tips inside the book.   
* Your submission should be your completed notebook. You can submit either through a HTML or link to a private GitHub repo.   
* Please let your instructors know if it is taking an excessive amount of time. The scripts do run long on 1M rows ~ a number of hours on the both types of VM's, but the development should not take an excessive amount of time.  
* The final section in the book shows a number of tasks, you need only complete 1 of them.   
* **For turning in your work**, please send instructors the link your repo containing your completed notebooks and information on V100 runtimes etc., alternatively, mail instructors the notebooks in html format along with runtimes. 
  
### AWS Limits

AWS by default do not give access to powerful GPUs by default. You need to request to have your service limit increased and specify the region you want to use.
This is the same for spot or on demand instance. It usually takes about a day or two for AWS to increase it. Specify you will need access to single `p3.2xlarge` and you will use spot pricing.
You can check out this : https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html
  
### Start your VMs and notebook as below.  
    
Use this command to pick out your default vpc, note, it is the vpc with `"IsDefault": true`.
```
aws ec2 describe-vpcs | grep VpcId
```
My one is `vpc-e4e35381`, I shall use this below. 

Now create a security group which will allow us to login and expose a port for a Jupyter notebook to be run. 
```
aws ec2 create-security-group --group-name hw06 --description "HW06" --vpc-id vpc-e4e35381
```
My one is `sg-09ceb02f960da25fa`, I shall use this below. 

Now take the security group which we have just created and open the ports for inbound and outbound traffic. 
```
aws ec2 authorize-security-group-ingress --group-id  sg-09ceb02f960da25fa   --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id  sg-09ceb02f960da25fa  --protocol tcp --port 8888 --cidr 0.0.0.0/0
```

We will not use docker here, instead we will use the Deep Learning AMI provided by Amazon. During the following steps you will need to accept the terms and conditions of the Deep Learning AMI you use, you will be provided a link where you can accept this. 
First let’s find a deep learning AMI in your region. You can replace the region I chose with your own. Please make sure your default region has `p3.2xlarge` instances available, if not, you may need to change regions.    
Use this to pick your deep learning AMI id. 
```
aws ec2 describe-images  --filters  Name=name,Values='Deep*Learning*Ubuntu*18.04*32*'
```
For example mine is : `"ImageId": "ami-0f5ebd171c26abc61"` 

Now lets look at the spot pricing on the `p3.2xlarge`. Spot pricing provide a significant discount over on demand pricing. However as the price fluctuates, we need to set a limit which we are willing to pay. I would recommend approximately 50% over the spot price. You can see the spot pricing using the below command. 
```
aws --region=eu-west-1 ec2 describe-spot-price-history --instance-types  p3.2xlarge --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'
```

At time of writing, the spot pricing is just under $1 per hour, so I set the limit at $1.50. Similar to week02 homework, enter the below in a file called `spot-options.json` in your current directory. 
```
{
  "MarketType": "spot",
  "SpotOptions": {
    "MaxPrice": "1.50",
    "SpotInstanceType": "one-time"
  }
}
```

Now lets start the image. 

```
aws ec2 run-instances --image-id ami-0f5ebd171c26abc61 --instance-type p3.2xlarge --security-group-ids sg-09ceb02f960da25fa  --associate-public-ip-address --instance-market-options file://spot-options.json --key-name darraghaws
```

If you do not get approval for spot capacity, you can try without spot pricing [do this only if the above `aws ec2 run-instances...` does not work],

```
aws ec2 run-instances --image-id ami-0f5ebd171c26abc61 --instance-type p3.2xlarge --security-group-ids sg-09ceb02f960da25fa  --associate-public-ip-address --key-name darraghaws
```
     
Again, it will take a couple of minutes to create. You can get the server address by using the below. 
```
aws ec2 describe-instances | grep ec2   
```
    
We will also need our public IP later for running Jupyter. `aws ec2 describe-instances | grep PublicIp`
My public ip is `54.194.227.21`


Now we login, 
```
ssh -i "darraghaws.pem" ubuntu@ec2-54-194-227-21.eu-west-1.compute.amazonaws.com
```
    
All the following steps are in the VM until you enter the jupyter URL in your browser.    
You will get a message like below on logging in. 
```
Please use one of the following commands to start the required environment with the framework of your choice:
for MXNet(+Keras2) with Python3 (CUDA 10.1 and Intel MKL-DNN) ____________________________________ source activate mxnet_p36
for MXNet(+Keras2) with Python2 (CUDA 10.1 and Intel MKL-DNN) ____________________________________ source activate mxnet_p27
for MXNet(+AWS Neuron) with Python3 ___________________________________________________ source activate aws_neuron_mxnet_p36
for TensorFlow(+Keras2) with Python3 (CUDA 10.0 and Intel MKL-DNN) __________________________ source activate tensorflow_p36
for TensorFlow(+Keras2) with Python2 (CUDA 10.0 and Intel MKL-DNN) __________________________ source activate tensorflow_p27
for Tensorflow(+AWS Neuron) with Python3 _________________________________________ source activate aws_neuron_tensorflow_p36
for TensorFlow 2(+Keras2) with Python3 (CUDA 10.1 and Intel MKL-DNN) _______________________ source activate tensorflow2_p36
for TensorFlow 2(+Keras2) with Python2 (CUDA 10.1 and Intel MKL-DNN) _______________________ source activate tensorflow2_p27
for TensorFlow 2.3 with Python3.7 (CUDA 10.2 and Intel MKL-DNN) _____________________ source activate tensorflow2_latest_p37
for PyTorch 1.4 with Python3 (CUDA 10.1 and Intel MKL) _________________________________________ source activate pytorch_p36
for PyTorch 1.4 with Python2 (CUDA 10.1 and Intel MKL) _________________________________________ source activate pytorch_p27
for PyTorch 1.6 with Python3 (CUDA 10.1 and Intel MKL) __________________________________ source activate pytorch_latest_p36
for PyTorch (+AWS Neuron) with Python3 ______________________________________________ source activate aws_neuron_pytorch_p36
for Chainer with Python2 (CUDA 10.0 and Intel iDeep) ___________________________________________ source activate chainer_p27
for Chainer with Python3 (CUDA 10.0 and Intel iDeep) ___________________________________________ source activate chainer_p36
for base Python2 (CUDA 10.0) _______________________________________________________________________ source activate python2
for base Python3 (CUDA 10.0) _______________________________________________________________________ source activate python3
```
We want the pytorch version 1.6 for this exercise. This has the pytorch native version of mixed precision available. Lets activate this. 
```
source activate pytorch_latest_p36
```
**You will need to `source` this, like above, each time you login.** 

Now in the server, lets get the packages we need before starting our homework.
```
pip install transformers
git clone https://github.com/MIDS-scaling-up/v2 w251
```

Lets start our Jupyter notebook.   
```
cd w251/week06/hw/
jupyter notebook --ip=0.0.0.0 --no-browser
```


You will get a message like below. 
```
[I 14:49:26.343 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 14:49:26.347 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///home/ubuntu/.local/share/jupyter/runtime/nbserver-16772-open.html
    Or copy and paste one of these URLs:
        http://ip-172-31-30-27:8888/?token=37b8bba7d420a4073b0a2169a24a995cde3ede8329f5ef9b
     or http://127.0.0.1:8888/?token=37b8bba7d420a4073b0a2169a24a995cde3ede8329f5ef9b
```

To access the book use the public ip found above along with the URL, like follows : http://54.194.227.21:8888/?token=37b8bba7d420a4073b0a2169a24a995cde3ede8329f5ef9b

Once in here, you will see the `BERT_classifying_toxicity.ipynb` - you can modify this to do the homework.  

Sometimes the jupyter session drops, you can leave it permanently up by running it in background like below. To get the url and token, just `cat nohup_log.out`.   
```
nohup jupyter notebook --ip=0.0.0.0 --no-browser &> nohup_log.out &
```

If you would like to kill the nohup session later, you can use `lsof | grep nohup_log.out` to find which pid is using this file. Then kill that pid. 
For example, if your ouput is like below, you should run `kill 16772` and `kill 16820`, 
```
ZMQbg/0   16772 16822          ubuntu    2w      REG              202,1     2231     539934 /home/ubuntu/w251/week06/hw/nohup_log.out
ZMQbg/1   16820                ubuntu    1w      REG              202,1     2231     539934 /home/ubuntu/w251/week06/hw/nohup_log.out
ZMQbg/1   16820                ubuntu    2w      REG              202,1     2231     539934 /home/ubuntu/w251/week06/hw/nohup_log.out
```



### Terminate your VM.   

At the end, make sure to terminate your VM.     
```
aws ec2 describe-instances | grep InstanceId
```
Pick up the instance ID and terminate it.   
```
aws ec2  terminate-instances --instance-ids i-07aaaa64804129136
```

Also, keep an eye on your costs, update the below date to the month your are running it. 
```
aws ce get-cost-and-usage \
    --time-period Start=2020-10-01,End=2020-10-31 \
    --granularity MONTHLY  \
    --metrics "BlendedCost" "UnblendedCost" 
```
### Raise usage limits on your account
We will be using 4 [T4](https://www.nvidia.com/en-us/data-center/tesla-t4/)'s in HW09 which is delivered through a g4dn.2xlarge instance. Please raise a limit request for using 32 VCPUs which will enable a `g4dn.2xlarge` instance in the region of your choice (preferably your default region in AWS). You can request an on-demand instance. The `Limits` option can be found in the ec2 dashboard of AWS - it is the fourth option, just below `EC2 dashboard`.   
If a quota increase via the service quota console is denied, please try submitting a service quota increase via the support console and provide the reason for the quota increase.   
An approved request is not a prerequisite for completing this homework 09, but please have the request submitted in the `EC2 dashoard`.   
A sample message for request increase below:
```
Please update the limit for VCPU on my account to be 32 for the g4dn.2xlarge instance type. We are currently running a graded homework in our class at UC Berkeley for the Master in Data Science program about training a Transformer-based Machine Translation network on a small English to German WMT corpus and it uses distributed computing across 4 EC2 instances.
```
