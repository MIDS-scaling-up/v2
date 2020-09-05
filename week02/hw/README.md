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

-   Click on Add User

    -   Set the User Name
    -   Select both Access Types (`Programmatic` and `AWS Management Console`)
    -   Accept the defaults for the password settings
    -   Click the "Next" button
    -   Create a Group
    -   Give your group a name
    -   **select `AdministratorAccess` role**)
    -   Ensure that your new group is selected, then click the "Next" button
    -   Do not add any Tags
    -   Click the "Create User" button
    -   Select to have User Access and Secret Key created and download
        the details to xls
    -   On your workstation (Mac or windows), download, install and configure
        AWS CLI-v2 using the new User credentials you just created.
        Follow the instructions from the link below.

        <https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html>

-  Go to Services-EC2-Keypairs

-  Create new keypair and download the .pem file
```
# Once downloaded, adjust the permissions of the pem file on your workstation
# Run this command to remove permissions from other users:
chmod 400 *.pem file 
```

-   Add the downloaded key pair to SSH identities on your workstation.
```
ssh-add -K "your_keypair.pem" 
ssh-add -L
```   

# Launch and Test Key AWS Resources

#### Create Default VPC
```
aws ec2 create-default-vpc
aws ec2 describe-vpcs | grep VpcId
# find the vpc-id of the one you just created
```
**NOTE: If you receive an UnauthorizedOperation error when creating the default VPC, ensure that you added the AdministratorAccess role to the Group you created above**

#### Create Public and Private security groups
```
# Use the VpcId from the previous step
aws ec2 create-security-group --group-name PublicSG --description "Bastion Host Security group" --vpc-id vpc-XXXXXXXX

# Extract GroupID of the Public security group created in the previous step
aws ec2 describe-security-groups | grep -A4 PublicSG | grep GroupId 

# If you do not see a GroupID, try this:
aws ec2 describe-security-groups | grep -A20 PublicSG | grep GroupId

# Use the VpcId from the previous step
aws ec2 create-security-group --group-name PrivateSG --description "Private instances Security group" --vpc-id vpc-XXXXXXXX

# Extract GroupID of the Private security group created in the previous step
aws ec2 describe-security-groups | grep -A4 PrivateSG | grep GroupId

# If you do not see a GroupID, try this:
aws ec2 describe-security-groups | grep -A20 PrivateSG | grep GroupId
```

#### Add SSH Ingress rule to Security groups
Using the Public and Private Security Group IDs from the previous step, authorize ssh ingress to the Security Groups:
```
aws ec2 authorize-security-group-ingress --group-id YOUR_PUBLIC_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress --group-id YOUR_PRIVATE_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
```

#### Launch Bastion EC2 Instance(JumpBox) into the public Security Group
Use Ubuntu AMI on t2.micro instance(free tier) in the default VPC.  
Replace the string `YOUR_KEY_NAME` with the name of your key pair created above. You can find it using the command `aws ec2 describe-key-pairs | grep KeyName`.

```
# Create the instance
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids YOUR_PUBLIC_GROUP_ID --associate-public-ip-address --key-name YOUR_KEY_NAME

# Retrieve the Public DNS name
aws ec2 describe-instances | grep PublicDnsName
```
    
If you get a message that the image is not available - `The image id '[ami-0bcc094591f354be2]' does not exist` - it could be that the image is not available in your conifgured region. 

You can pick an image in your region, by running the below, 

```
aws ec2 describe-images  --filters  Name=name,Values='ubuntu/images/hvm-ssd/ubuntu-bionic-18.04*' Name=architecture,Values=x86_64   | head -100
```

#### Launch Private EC2 instance into Private Security Group using Ubuntu
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids YOUR_PRIVATE_GROUP_ID --key-name YOUR_KEY_NAME

# Retrieve the PublicDnsName of the new instance
aws ec2 describe-instances | grep PublicDnsName

```
#### SSH into Baston Host first and then to the Private instance
```
# From your workstation
ssh -A ubuntu@YOUR_PUBLIC_EC2_NAME.compute-1.amazonaws.com

# Then ssh from the bastion host to the private instance
ssh ubuntu@YOUR_PRIVATE_EC2_NAME.compute-1.amazonaws.com
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

### Pricing
    
#### Spot pricing

As we have limited credit for aws instances, it makes sense to use spot instances which are cheaper than on demand instances.  
With Spot Instances, you pay the Spot price that's in effect for the time period your instances are running. Spot Instance prices are set by Amazon EC2 and adjust gradually based on long-term trends in supply and demand for Spot Instance capacity.   
   
On demand pricing for all instances can be seen at https://aws.amazon.com/ec2/pricing/on-demand/     
At time of writing a t2.large instance costs $0.1008 per Hour in Europe(Ireland) or eu-west-1.    

We can check the equivalent spot price for this instance. Please change the region to your local region - this will shown in `aws configure get region` if you have it set. 
```
aws --region=eu-west-1 ec2 describe-spot-price-history --instance-types t2.large --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'
```
You should see it is cheaper than the on demand rate, below is an example of one price at time of writing, so over 3 times cheaper!!
```
    {
        "az": "eu-west-1b",
        "price": "0.030200"
    },
```

To provision an instance with spot pricing, create a file in your current directory named `spot-options.json` and place the below inside it, where you configure max price a little above the spot pricing. Spot pricing fluctuates, so leave some buffer. 
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

#### Monitor your billing
Please keep an eye on your costing through the semester with the below command. Students have run over in the past.    
```
aws ce get-cost-and-usage \
    --time-period Start=2020-07-01,End=2020-07-31 \
    --granularity MONTHLY  \
    --metrics "BlendedCost" "UnblendedCost"   
```

### Turn in
Please send a message on the class portal homework submission page indicating that you were able to set up the above instances, and have them terminated.   


