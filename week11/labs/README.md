# TurboVNC on your TX2

This lab will allow you to run a VNC server on your TX2 that works with OpenGL. Essentially, you can run the homework remotely. The .deb files are hosted in this github repo.

```
dpkg --add-architecture aarch64
sudo dpkg -i libjpeg-turbo_2.0.1_arm64.deb
sudo dpkg -i virtualgl_2.6.2_aarch64.deb
sudo dpkg -i turbovnc_2.2.1_aarch64.deb
sudo apt install xfce4 xfce4-goodies
```

Add the following to /etc/X11/xorg.conf

```
Section "Screen"
    Identifier  "Screen0"
        Option "AllowEmptyInitialConfiguration"
        Option "UseEdid" "False"
EndSection
```

Create the file `/etc/ld.so.conf.d/libjpeg-turbo.conf` and add the following line

```
/opt/libjpeg-turbo/lib32
```

Run the following commands:

```
sudo ldconfig
sudo /opt/VirtualGL/bin/vglserver_config
sudo usermod -a -G vglusers nvidia
```

Create the file `~/.vnc/xstartup.turbovnc` and add the following:

```
#!/bin/sh

unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4 &
```

Start the VNC server with `/opt/TurboVNC/bin/vncserver`

You can connect to the VNC server with any VNC client, but you will need the TurboVNC client for OpenGL to work properly.

Connect to the VNC server at <your_jetson_ip_address>:1
