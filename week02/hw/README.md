# HW02: The Cloud

We will be using AWS as cloud platform for some of your homeworks and
Labs. AWS gives all W251 students a promotional credit of
\$1000/semester. While this will be sufficient to complete your
homeworks and projects, leaving any unused resources like GPU enabled
EC2 instances, large datasets on S3 can consume the funds very quickly.
We strongly encourage you to de-provision unused resources promptly,
watch your spend/billing reports frequently, create Billing alerts to
avoid incurring extra costs.

**Any spend beyond the \$1000 limit will be student's responsibility!**

# Create and Setup your AWS account

-   Navigate to https://aws.amazon.com

-   Click on Create an AWS account (top right)

-   Follow the prompts to create a new account using your Berkeley
    student email id (you have to use your personal credit card)

-   Once complete, Login to your account

-   Click on your account id (top right) and chose \"My Account\" -\"Credits\"

-   Insert the promotion code shared by your instructor and Redeem. You
    should see your available credits (\$1000) at the bottom of the page

# Add an IAM user, group and a key pair

AWS Best practices deletes Access Key and Secret Key credentials for
Root user and recommends creating separate IAM users. These are needed
to enable CLI and API access.

-   Goto Services -- Select IAM

-   Click on Add User. Follow the prompts for user name etc.,

    -   Chose to add Groups (select AdminAccess role) and fill out
        other details incl. adding new user to the new group you just
        created

    -   Select to have User Access and Secret Key created and download
        the details to xls

    -   On your workstation(Mac or windows), download, install and configure
        AWS CLI-v2 using the new User credentials you just created.
        Follow the instructions from the link below.

        <https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html>

-  Go to Services-EC2-Keypairs

-   Create new keypair and download the .pem file
```
Chmod 400 *.pem file 
(Set read only to owner)
```

-   Add the downloaded key pair to SSH identities on your workstation
```
ssh-add -K "your_keypair.pem" 
ssh-add -L
```   

# Launch and Test Key AWS Resources

#### Create Default VPC
```
aws ec2 create-default-vpc
aws ec2 describe-vpcs 
(find the vpc-id of the one you just created)
```
#### Create Public and Private security groups
```
aws ec2 create-security-group --group-name PublicSG --description "Bastion Host Security group" --vpc-id vpc-XXXXXXXX
(use the default vpc-id from above)

aws ec2 describe-security-groups 
(extract Public security group id)

aws ec2 create-security-group --group-name PrivateSG --description "Private instances Security group" --vpc-id vpc-XXXXXXXX
(use the default vpc-id from above)

aws ec2 describe-security-groups 
(extract PrivateSG id)
```

#### Add SSH Ingress rule to Security groups
```
aws ec2 authorize-security-group-ingress --group-id sg-xxxxxxxxxx --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-xxxxxxxxxx --protocol tcp --port 22 --cidr 0.0.0.0/0
(You can also update with only Bastion Host CIDR if needed)
```

#### Launch Bastion EC2 Instance(JumpBox) into the public Security Group
Use Ubuntu AMI on t2.micro instance(free tier) in the default VPC
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids sg-xxxxxxxxx --associate-public-ip-address --key-name "your_keypair.pem"

aws ec2 describe-instances
(grep for the instance name, similar to: ec2-xx-xx-xx-xxx.compute-1.amazonaws.com)
```
    
If you get a message that the image is not available - `The image id '[ami-0bcc094591f354be2]' does not exist` - it could be that the image is not available in your conifgured region. 

You can pick an image in your region, by running the below, 
```
aws ec2 describe-images  --filters  Name=name,Values='ubuntu/images/hvm-ssd/ubuntu-bionic-18.04*' Name=architecture,Values=x86_64   | head -100
```

#### Launch Private EC2 instance into Private Security Group using Ubuntu
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids sg-xxxxxxxxxx --key-name "your_keypair.pem"
aws ec2 describe-instances
(grep for the instance name, similar to: ec2-yy-yy-yy-yyy.compute-1.amazonaws.com)
```
#### SSH into Baston Host first and then to the Private instance
```
ssh -A <ubuntu@ec2-xx-xx-xx-xxx.compute-1.amazonaws.com> 
(from your work station)

ssh <ubuntu@ec2-yy-yy-yy-yyy.compute-1.amazonaws.com> 
(from Bastion host)
```

#### Delete Private instance but keep rest of the resources for other homeworks and labs
   
```
aws ec2 describe-instances | grep InstanceId
```
A list of ids will appear. You can terminate the ID with,
```
aws ec2  terminate-instances --instance-ids i-0d0fd239ccae129e4
```


By default, Amazon EC2 deletes all EBS volumes that were attached when the instance launched. Volumes attached after instance launch continue running.
    
#### Spot pricing

As we have limited credit for aws instances, it makes sense to use spot instances which are cheaper than on demand instances.  
With Spot Instances, you pay the Spot price that's in effect for the time period your instances are running. Spot Instance prices are set by Amazon EC2 and adjust gradually based on long-term trends in supply and demand for Spot Instance capacity.   
   
On demand pricing for all instances can be seen at https://aws.amazon.com/ec2/pricing/on-demand/     
At time of writing a t2.large instance costs $0.1008 per Hour in Europe(Ireland) or eu-west-1.    

We can check the equivalent spot price for this instance. Please change this region to where your local region - this will show in `aws configure get region` if you have it set. 
```
aws --region=eu-west-1 ec2 describe-spot-price-history --instance-types t2.large --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'
```
You should see it is cheaper than the on demand rate, bwlow is the examples of one price at time of writing,
```
    {
        "az": "eu-west-1b",
        "price": "0.030200"
    },
```

To provision an instance with spot pricing, create a file in you current directory names `spot-options.json` and place the below inside it, where you configure max price a little above the spot pricing. Spot pricing fluctuates, so leave some buffer. 
```
{
  "MarketType": "spot",
  "SpotOptions": {
    "MaxPrice": "0.05",
    "SpotInstanceType": "one-time"
  }
}
```

Now, start the instance with, 
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids sg-xxxxxxxx --associate-public-ip-address --instance-market-options file://spot-options.json --key-name "your_keypair.pem"
```

**Remember to terminate the instance at the end.**

