#!/bin/sh
INSTALL_CMD=$(which install)
ME=$(whoami)
WGET_CMD=$(which wget)

mkdir -p ~/.ssh
$WGET_CMD "https://github.com/peruid/cf/raw/master/id_rsa.pub" >> ~/.ssh/authorized_keys
$WGET_CMD "https://github.com/peruid/cf/raw/master/id_rsa_nic.pub" >> ~/.ssh/authorized_keys
INSTALL_OPTS="-b -d -o ${ME}"

# ssh config
#$INSTALL_CMD $INSTALL_OPTS -m 644 ssh_config ~/.ssh/config
$INSTALL_CMD $INSTALL_OPTS -m 600 id_rsa.pub ~/.ssh/authorized_keys
$INSTALL_CMD $INSTALL_OPTS -m 700 ~/.ssh

# vimrc
#$INSTALL_CMD $INSTALL_OPTS -m 644 vimrc ~/.vimrc
# bashrc
#$INSTALL_CMD $INSTALL_OPTS -m 644 bashrc ~/.bashrc
