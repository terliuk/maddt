#! /bin/sh
## simple script to setup the grid environment (icecube VO)
## Usage: source grid_icecube.sh
## Make sure, usercert.pem, userkey.pem are in your $HOME/.globus

voms-proxy-init -hours 192 -verify -debug -voms icecube
myproxy-init -c $((30*24)) -n -Z $USER

