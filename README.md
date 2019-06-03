# W251 reloaded (Spring 2019)

The revised class is focused on Deep Learning and Big Data at the Edge and in the Cloud.

To follow the class, you'll a Mac or a PC (Windows or Linux) with an ability to run docker or VirtualBox VMs. You will also need additional equipment as follows:
### Required equipment:

1. Nvidia [Jetson TX2 dev kit](https://developer.nvidia.com/embedded/buy/jetson-tx2) ($299 + tax with educational discount). To get the discount, you'll need a code, which you can get from [Nvidia directly](https://www.nvidia.com/object/jetsontx2-edu-discount.html) or by signing up for the class or contacting your instructor(s).  We are currently testing [Nvidia Xavier](https://developer.nvidia.com/embedded/buy/jetson-xavier-devkit) and you're welcome to give it a shot, but it's expensive ($1,299 AFTER the educational discount), while the software (Jetpack) for it is not yet GA.  You've been warned. 

2. Additional storage.  The Jetson TX2 System on a Chip (SoC) has only 16G eMMC, which is tight for developer.  There is a slot for an SD card and it could be the cheapest (albeit, a somewhat slow) option.  The class will take advantage of Docker which in turn drive up storage needs.  We recommend at least 128 GB, for instance, [this card](https://www.amazon.com/Sandisk-Ultra-128GB-Micro-Adapter/dp/B073JYC4XM/ref=sr_1_4?s=electronics&ie=UTF8&qid=1537913441&sr=1-4&keywords=micro+sd+card+128gb) (currently, $19.99).  If you are a performance user, you will need to get a SATA SSD, e.g. [this one](https://www.amazon.com/Kingston-240GB-Solid-SA400S37-240G/dp/B01N5IB20Q/ref=sr_1_3?s=electronics&ie=UTF8&qid=1543808366&sr=1-3&keywords=240GB+SSD) (currently, $35.50). While it's possible to insert an SSD directly / vertically into the Jetson dev board, it's quite easy to accidentally bump the SSD causing the slot to break off the board.  Therefore, it's safer to purchase a [cable connector](https://www.amazon.com/gp/product/B00L9R3AKA/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) (currently, $5.66). Alternatively, you could just use any USB 3.0 external disk.

3. A external webcam.  The TX2 does have an onboard camera, but it has always had compatibility issues. So a USB webcam is a safe option, e.g. [this cheap camera](https://www.amazon.com/Sea-Wit-Recording-Computer-External/dp/B074252LWL/ref=sr_1_9?s=electronics&ie=UTF8&qid=1537913528&sr=1-9&keywords=usb+webcam).  Note that this particular webcam is not HD, even though it's advertised as such and you may want to go with a [true HD webcam](https://www.amazon.com/Logitech-Widescreen-Calling-Recording-Desktop/dp/B006JH8T3S/ref=sr_1_3?ie=UTF8&qid=1544053053&sr=8-3&keywords=hd+usb+webcam) instead. But, true HD is not required for the class.

4. A USB 3.0 switch .  Here's [the one I am happy with](https://www.amazon.com/gp/product/B00TPMEOYM/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) (currently, $9.89)  If you are using Xavier, you'll need [this one instead](https://www.amazon.com/gp/product/B07GGMYDCW/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)

5. You will also need a mouse, keyboard, a monitor and an HDMI cable to connect to the monitor.  The tx2 has wifi built in or a wired connection is preferred if you'll be doing a lot of video processing.

6. While we have not had any issues, [an ant-static wrist strap](https://www.amazon.ca/Anti-Static-Wrist-Straps-Anti-Static/dp/B017164JHA) is never a bad idea.

### Homeworks:
A homework is due before each class.  There are two types of homeworks: graded and credit only. Here is the link to [class 1](week01) - be sure to complete the setup of your Jetson as described in [homework 1](week01/hw)

### SSH Reminder:
Ensure that any VSI/VM create prohibts login with password prohibited.
See: https://github.com/MIDS-scaling-up/v2/tree/master/week02/hw/README.md for details.

### Graded homeworks
The graded homeworks are week 3, week 6, week 9, week 11; please notice that those are the slots that are available on the ISVC website except there are labeled as Homework 1, 2, 3 and 4 (we are working on getting this changed but in the meantime submit matching the graded homework week with it's slot i.e week 3 uploaded to Homework 1).


