### This lab will follow on from the homework and build a 1d-CNN

#### Ordering an instance from the image template you built in week02
Access the IBM® Cloud infrastructure [customer portal](https://control.softlayer.com/) by using your unique credentials.
1. Access the Image Templates page by selecting Devices > Manage > Images.
2. Select the image you created in week02/lab2. If you have not created one there you may select the public image `w251_nvidia_p100`
3. Click the Actions menu for the image template that you want to use and select the type of virtual server that you want to order. Please select `flavor AC1.8x60x100`. 
4. On the Configure your Cloud Server page, complete all of the relevant information.
5. Click the Add to Order button to continue.
6. On the Checkout page, select flavor **** and complete any advanced system configuration.
7. Click the Cloud Service terms and the Third-Party Service Agreement check boxes.
8. Confirm or enter your payment information and click Submit Order. You are redirected to a screen with your provisioning order number. You can print the screen because it's also your provisioning order receipt.

#### Start the Jupyter notebook.

Log in to your VM, and check CUDA is installed.   
```
# On command line
nvidia-smi
```
   
Now lets build our docker with the jupyter notebook.  
Once in, start running your notebook and follow the instructions in bold where to fill in code. 
```
docker run --rm --runtime=nvidia -it -p 8888:8888 w251/tensorflow_gpu_lab04:latest
```
