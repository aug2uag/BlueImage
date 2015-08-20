#! /usr/bin/python
# coding: utf-8
import os
import time
import subprocess

timestamp = int(time.time())
imageName = "image"
namespace = "default"
container = "cont_" + str(timestamp)

cmd1 = "ice --cloud build -t " + imageName + " ."
cmd2 = "ice --local tag " + imageName + " registry.ng.bluemix.net/" + namespace + "/" + imageName
cmd3 = "ice --local push registry.ng.bluemix.net/" + namespace + "/" + imageName
cmd4 = "ice run –name " + container + " -p 80 " + namespace + "/" + imageName

# get previous container name and IP addr
p = subprocess.Popen(["ice", "--cloud", "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
oldContainer = out.split()[13]
ipAddress = out.split()[19]

cmd5 = "ice ip unbind " + ipAddress + " " + oldContainer
cmd6 = "ice ip bind " + ipAddress + " " + container

for i in [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]:
	os.system(i)