# Kaggle labs

### Kaggle Notebooks inference and TTA
    
If you have not done so, please sign up to [kaggle.com](kaggle.com)    
    
Go to the kernel we will be working with today [week07 lab](https://www.kaggle.com/darraghdog/berkeley-mids-w251-week7-lab).   
   
Fork the Kernel – using the “Copy and Edit Kernel” option found in the top right corner (you will see it after clicking on the three dots). Please ensure you have the accelerator set to GPU as seen below.   
![](kaggle_accelerator_setting.png?raw=true "Title"){:height="300px" width="250px"}
     
The training steps will run too long so we skip these steps, and run until only until cell 27 where we set up training with mixed precision. We will skip over sections 28 to 29 as they run too long.   

Now skip forward to the section “Now please implement test time augmentation to make predictions”.
Your task in here is to,
* Load the `recursion_model.bin` weights into the model. Note; you may need to change the folder where the weights are located. Check subdirectories within directory `../input`    
* Turn the torch model to evaluation mode.   
* Iterate through the valloader and view a sample image. You do not need to view it as an image; it suffices to check the shape of the batch and print some of the contents, to see for example is it already normalised etc.      
* Predict on a single image.   
* Apply augmentation to the image; eg. horizontal flip, or vertical flip, using albumentations library. You can reference how augmentation is performed during training.        
* Perform Test Time Augmentation (TTA) by predicting on the original image, and the augmentations and averaging the result.   

Finally after the above steps, predict on all images using TTA and save your predictions. 
