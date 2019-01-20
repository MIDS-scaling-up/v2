# Homework 2: The Cloud

## Add a ssh key to the Cloud Portal
 - Create a ssh key on your local computer, if you don't have one, using the ssh-keygen command
 - Navigate to https://control.softlayer.com
 - Log in using your credentials or using your IBM ID (if that's how you configured your account)
 - Navigate to Devices -> Manage -> SSH Keys
 - Use the "Add" link to add your public ssh key to the portal

## Enable VLAN spanning
 - Navigate to Network -> IP Management -> VLANs
 - Click on the "Span" tab
 - Turn `VLAN Spanning` On

## Create a VSI using the gui (make sure ssh key is used)
 - Navigate to https://cloud.ibm.com/classic/devices
 - Select the blue "Order Devices" button at the top right
 - Select "Virtual Server" from the list, then "Public Virtual Server"
 - Accept the default for Quantity (1) and Billing (Hourly)
 - Choose a hostname and domain. You can literally use any domain name you choose, it will not be registered in DNS
 - Choose a location near you
 - Select the Compute C1.1x1 profile (1 CPU, 1GB of RAM)
 - Select your SSH Key from the dropdown list
 - Choose Ubuntu 18.04 Minimal as your Image
 - Accept the rest of the defaults
 - Read and Accept the Service Agreements (if you agree with them) and click the Create button
 - Your Virtual Machine (also called a Virtual Server Instance) will appear in the portal
 - Navigate to https://cloud.ibm.com/classic/devices to monitor your VM creation

## Harden the VSI, ensure ssh still works with the key
 - SSH into the VSI using your SSH Key and the `root` ID
 - Edit /etc/ssh/sshd_config and make the following changes to prevent brute force attacks

```
PermitRootLogin prohibit-password
PasswordAuthentication no
```
 - Restart the ssh daemon: `service sshd restart`
 - Ensure that you can only login with a ssh key and that password authentication is properly disabled:

```
ssh admin@localhost
```
 - It should reject your ssh request


## Install IBM Cloud CLI on the VSI

Copy and paste the following command to a terminal of your Linux OS and run it:

```
curl -fsSL https://clis.ng.bluemix.net/install/linux | sh
```

Log into IBM Cloud using `ibmcloud login`

Enable the IBM Cloud Infrastructure component using `ibmcloud sl init` (accept the default endpoint)

Test the CLI using the command `ibmcloud sl vs list` to see a list of VSIs in your account


## Create a VSI using the CLI with private network only

Create a new ssh key on your VSI using `ssh-keygen`

Add the new key to the IBM Cloud portal using the command:

```
ibmcloud sl security sshkey-add MyNewKey --in-file ~/.ssh/id_rsa.pub
```

Use the following command to retrieve your new SSH Key ID:

```
ibmcloud sl security sshkey-list
```

Use the following command to create a new VSI in your account, **ensuring to replace the key ID with your SSH Key ID**:

```
ibmcloud sl vs create --hostname=test --private --domain=you.cloud --cpu=2 --memory=2048 --datacenter=ams03 --os=UBUNTU_16_64 --san --disk=100 --key=123456
```

## Connect to the new VSI using the original VSI as a jumpbox

Use the following command to find the Private IP address of your new VSI:

```
ibmcloud sl vs list
```

Connect to the new VSI using ssh 

Once you have verified that you can connect to the new VSI, you can disconnect and cancel it using the `ibmcloud sl vs cancel` command. You will need to provide an argument to cancel the proper VSI. **DO NOT CANCEL YOUR PRIMARY, ORIGINAL VSI. YOU WILL NEED IT IN FUTURE HOMEWORKS**

Ensure you successfully cancel the VSI using the `ibmcloud sl vs list` command

**To Turn In**: A copy/paste of the output from `ibmcloud sl vs list` before and after you cancel the second VSI

