#! /usr/bin/python
# coding: utf-8
import os
import re
import subprocess

agg = []

# get previous container name and IP addr
p = subprocess.Popen(["ice", "--cloud", "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
oldContainer = re.findall(r'\d+|\D+', out.split()[13])
nameCounter = oldContainer[1] if len(oldContainer) > 1 else 0
oldContainer = oldContainer[0]
ipAddress = '111.111.111.111'

imageName = "image"
namespace = "default"
container = "cont_" + str(nameCounter)

agg.append("ice --cloud build -t " + imageName + " .")
agg.append("ice --local tag " + imageName + " registry.ng.bluemix.net/" + namespace + "/" + imageName)
agg.append("ice --local push registry.ng.bluemix.net/" + namespace + "/" + imageName)
agg.append("ice run –name " + container + " -p 80 " + namespace + "/" + imageName)

if ipAddress:
	agg.append("ice ip unbind " + ipAddress + " " + oldContainer)
	agg.append("ice ip bind " + ipAddress + " " + container)

for i in agg:
	os.system(i)
	# print(i)