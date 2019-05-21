## Lab 03 - Internet of things

### 1. Imitating a simple sensor
In this session's homework, you built a pipeline for detecting faces, transporting them to the cloud and storing them there. But in doing so, we skipped a step as IoT 101 is working with simple sensors!  Let's fill this gap.  In this lab, you goal is to propagate to the cloud the temperature of your GPU on the Jetson.

To generate the "sensor output", you can use the output of the ```tegrastats``` command, e.g.
```
RAM 1004/7852MB (lfb 7x2MB) CPU [0%@350,4%@345,2%@499,1%@341,1%@349,0%@345] EMC_FREQ 17%@40 GR3D_FREQ 0%@114 APE 150 MTS fg 0% bg 0% PLL@34C MCPU@34C PMIC@100C Tboard@28C GPU@32C BCPU@34C thermal@33.2C Tdiode@30.5C VDD_SYS_GPU 153/153 VDD_SYS_SOC 383/383 VDD_4V0_WIFI 0/0 VDD_IN 1876/1876 VDD_SYS_CPU 229/229 VDD_SYS_DDR 134/134
RAM 1004/7852MB (lfb 7x2MB) CPU [1%@346,4%@499,3%@499,0%@345,0%@345,0%@346] EMC_FREQ 17%@40 GR3D_FREQ 0%@114 APE 150 MTS fg 0% bg 0% PLL@34C MCPU@34C PMIC@100C Tboard@28C GPU@32C BCPU@34C thermal@33.2C Tdiode@30.25C VDD_SYS_GPU 153/153 VDD_SYS_SOC 383/383 VDD_4V0_WIFI 0/0 VDD_IN 1876/1876 VDD_SYS_CPU 229/229 VDD_SYS_DDR 115/124
RAM 1004/7852MB (lfb 7x2MB) CPU [0%@346,5%@806,4%@807,0%@345,0%@345,0%@345] EMC_FREQ 17%@40 GR3D_FREQ 0%@114 APE 150 MTS fg 0% bg 0% PLL@34C MCPU@34C PMIC@100C Tboard@28C GPU@32C BCPU@34C thermal@33.2C Tdiode@30.5C VDD_SYS_GPU 153/153 VDD_SYS_SOC 383/383 VDD_4V0_WIFI 0/0 VDD_IN 1876/1876 VDD_SYS_CPU 229/229 VDD_SYS_DDR 134/127
```
The GPU temperature is here: ```GPU@32C``` Your goal is:
* parse out the GPU temperature
* as soon as tegrastats produces the next value, publish it to the local broker.  You will need to specify a new topic for this, different from the one you used in your homework
* You will need a new forwarder, which will forward this to the cloud, again, to a different topic
* Finally, you need to be able to receive these messages in the cloud
* What if your connection was severed? How do you know the "last known good" value of the GPU temperature? You need to research the "retained" messages implementation in Mosquitto and add them to your processing pipeline.

### 2. Motion detection
Detecting faces is fun, but detecting motion could be even more fun.  Depending on their location, most of the frames that the surveillance cameras see contain absolutely nothing interesting. This lab is very similar to your homework, but instead of detecting faces, you should be detection areas of the frame where motion occurred and displaying bounding rectangles around them
Get the following code to run.  Your job is to implement the blur and then to display the frame. 
```
import numpy as np
import cv2

cap = cv2.VideoCapture(1)

fgbg = cv2.createBackgroundSubtractorMOG2()

while(1):
     ret, frame = cap.read()

     fgmask = fgbg.apply(frame)
     ## implement the blur function with the kernel of 3,3
     ## display the frame
     k = cv2.waitKey(30) & 0xff
     if k == 27:
         break

cap.release()
cv2.destroyAllWindows()
```

Can you figure out how to create a bounding rectangle around the frame?
