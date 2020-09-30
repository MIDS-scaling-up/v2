### Video Manipulation

In this lab we will learn,
1. How to scrape videos from youtube.   
2. How to store them as frames in python.  
3. How to manipulate the frames and makes an altered video.   

The notebook for you to go through is listed at the bottom.  
We show you how render the video from Erykah Badu's excellent, `Bag Lady`, in colab, like below.    
![](figs/original.gif)  
Your take will be to extract the faces from this clip, and render them side by side in a new video like below.   
![](figs/raw_bboxes.gif)  
If you get that far you did great. However, we see the faces are choppy. If you have time after ward you can try smoothing the bounding box sequences, like below.  
![](figs/smoothed_bboxes.gif)   
We used pandas rolling mean with a windows size of 12 to acieve this. Feel free to ask your instructor for the solution if you are stuck.    
