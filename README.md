# W251 reloaded (Spring 2019)

The revised class is focused on Deep Learning and Big Data at the Edge and in the Cloud.
### Recommended equipment:

1. Nvidia Jetson TX2 dev kit ($299 + tax with educational discount). To get the discount, you'll need a code, which you can get from [Nvidia directly](https://www.nvidia.com/object/jetsontx2-edu-discount.html) or by signing up for the class or contacting your instructor(s).

2. Additional storage.  The Jetson TX2 System on a Chip (SoC) has only 16G, which is tight for developer.  A slot for an SD card and it could be the cheapest (albeit, a somewhat slow) option.  The class will take advantage of Docker which in turn drive up storage needs.  We recommend at least 128 GB, for instance:


## 1. Nvidia Jetpack SDK
Jetpack is a SDK that basically contains everything needed for deep learning and AI applications in a handy package for the Jetson. Installation on the Jetson requires downloading and installing both on the Jetson (the target) and an Ubuntu computer (the host).
All of the following must be done in an Ubuntu OS. If a command is ever permission denied, try adding "sudo" at the beginning.
Refer to https://docs.nvidia.com/jetson/archives/jetpack-archived/jetpack-33/index.html for more detailed instructions (these are for Jetpack 3.3 on the Jetson TX2).

### Host (Computer) Installation
To reiterate, you will need a machine running Ubuntu 16.04 or Ubuntu 18.04. If you do not have one, you will need to create a VM running Ubuntu.

#### VM Installation (if needed)
Download Virtual Box [here](https://www.virtualbox.org/wiki/Downloads) and the extension to give VMs access to your USB hubs [here](https://download.virtualbox.org/virtualbox/5.2.14/Oracle_VM_VirtualBox_Extension_Pack-5.2.14.vbox-extpack). First download the Ubuntu 16.04 iso image [here](http://releases.ubuntu.com/16.04/ubuntu-16.04.5-desktop-amd64.iso). Open Virtual Box and select "New" in the upper left corner. Make sure the type and version are "Linux" and "Ubuntu 64-bit". When p
