#! /bin/bash
if [[ -z "$SSH_PORT" ]]; then
    echo "port not specified" 
    sudo /usr/sbin/sshd -D
else
   echo "port specified"
   echo "Host *" >> .ssh/config
   echo "  Port $SSH_PORT" >> .ssh/config
   sudo /usr/sbin/sshd -p $SSH_PORT -D
fi
