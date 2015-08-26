#! /usr/bin/python
# coding: utf-8
import os
import io
import sys
import json
import time
import pprint
import argparse

pp = pprint.PrettyPrinter(indent=4)

if not os.path.isfile('./config.json'):
	parser = argparse.ArgumentParser(description='IBM Bluemix Container \
		Management Instrument for Prototyping and Deployments',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(
		'--flag', '-f', required=False, type=int, 
		help='flag number current or init value\n \
		defaults to 0', default=0)
	parser.add_argument(
		'--ip', '-p', required=False, type=str, 
		help='optional public IP address')
	parser.add_argument(
		'--namespace', '-s', required=True, type=str, 
		help='designated namespace')
	parser.add_argument(
		'--directory', '-d', required=True, type=str, 
		help='absolute directory suggested')
	parser.add_argument(
		'--ports', '-r', required=True, type=int, nargs='+',
		help='space separated list of ports, include 80')
	parser.add_argument(
		'--image', '-i', required=False, type=str, 
		help='static image name\n \
		defaults to "xyz"', default='xyz')
	parser.add_argument(
		'--container', '-n', required=False, type=str, 
		help='static base container name\n \
		defaults to "bmContainer', default='bmContainer')
	parser.add_argument(
		'--url', '-u', required=False, type=str, 
		help='Bluemix base url, defaults to:\n \
		registry.ng.bluemix.net/',
		default='registry.ng.bluemix.net/')

	args = parser.parse_args()

	configs = {
		'flag': args.flag,
		'directory': args.directory,
		'ports': args.ports,
		'ip': args.ip,
		'namespace': args.namespace,
		'image': args.image,
		'container': args.container,
		'url': args.url
	}

	print('*** CONFIRMATION REQUIRED ***\
		\nplease confirm writing the following configurations to file:\n')
	pp.pprint(configs)
	print('\nReturn Y to proceed or anything else to exit')
	ans = raw_input()
	if ans.lower() != 'y':
		sys.exit()

	with io.open('config.json', 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(configs, 
						ensure_ascii=False, indent = 4)))

	print('*' * 40)
	print('Congratulations, configuration is completed. \
		  \nTo delete cartridge and images, run script without args: \
		  $ python image.py')
	sys.exit()


with open('config.json') as data_file:    
    data = json.load(data_file)

container = data['container']
directory = data['directory']
flag = data['flag']
image = data['image']
ip = data['ip']
namespace = data['namespace']
ports = data['ports']
url = data['url']

imageAddr = namespace + '/' + image + ':'

# 1 - stop old container
oldContainer = container + str(flag)
command = "ice stop " + oldContainer
# os.system(command)

# 2 - if ip, unbind
if ip is not None:
	command = "ice ip unbind " + ip + " " + oldContainer
	# os.system(command)


#3 - delete previous images
previousImageShort = imageAddr + str(flag)
previousImageLong = url + previousImageShort
command = "ice --local rmi " + previousImageShort
# os.system(command)
command = "ice --local rmi " + previousImageLong
# os.system(command)
command = "ice --cloud rmi " + previousImageShort
# os.system(command)

#4 - build, tag, push new image
newImageShort = imageAddr + str(flag + 1)
newImageLong = url + newImageShort
command = "ice --local build -t " + newImageShort + " " + directory
# os.system(command)
command = "ice --local tag " + newImageShort + " " + newImageLong
# os.system(command)
command = "ice --local push " + newImageLong

#5 - run new container
newContainer = container + str(flag + 1)
specifiedPorts = ''
for port in ports:
	specifiedPorts+='-p ' + str(port) + ' '
command = "ice run --name " + newContainer + " " + specifiedPorts + " " + newImageShort
# os.system(command)

#6 - if ip bind port to new container
if ip is not None:
	command = "ice ip bind " + ip + " " + newContainer
	# os.system(command)

#7 - delete old container
command = "ice rm " + oldContainer
# os.system(command)

data['flag']+=1

with io.open('config.json', 'w+', encoding='utf-8') as f:
	f.write(unicode(json.dumps(data, 
					ensure_ascii=False, indent = 4)))
