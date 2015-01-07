#!/usr/bin/python

import os
import os.path
import socket
import time
import base64 
import boto.ec2

#Functions:
def bootstrip(instance):
    print "Bootstrip instance.."
    time.sleep(1)

#Function - Check port reachable
def check_port(public_dns_name, port=22, timeout=5):
    print "Check Server %s Port %i .. (Timeout is %i seconds)" % (public_dns_name, port, timeout)
    try_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Setup timtout to x seconds before we make the connection:
    try_socket.settimeout(timeout)
    try:
        result = try_socket.connect((public_dns_name, port))
        print "Port %i reachable now!" % (port)
        try_socket.close()
        return 0 
    except socket.error as e:
        print "Error on connect: %s" % e
        try_socket.close()
        return 1
    

#Functions end

#Some Common Vars:
SCRIPT_NAME = os.path.basename(__file__)
USER = os.environ['USER']
BOOTSTRIP_FILE_NAME = './bootstrip.sh'

#Read Bootstrip File: 
BOOTSTRIP_FILE = open(BOOTSTRIP_FILE_NAME,'r')
bootstrip_file_contents = BOOTSTRIP_FILE.read()
BOOTSTRIP_FILE.close()

#Define:
#AWS China HVM: Amazon Linux AMI release 2014.09
ami = 'ami-ce46d4f7'

#Connect to region with profile 'cn'
conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn')
#conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn',debug=2)

#Define the network interface will be used inside VPC:
network_interface_config = boto.ec2.networkinterface.NetworkInterfaceSpecification(
        subnet_id                   = 'subnet-cc8b9bae',
        groups                      = ['sg-f59a8497'],
        description                 = "Created by Edanz CLI: ec2.py",
        delete_on_termination       = True,
        associate_public_ip_address = True
        )
network_interface = boto.ec2.networkinterface.NetworkInterfaceCollection(network_interface_config)


#Define the block device:
dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType()
dev_sda1.size = 10 
dev_sda1.delete_on_termination = True

block_device_map = boto.ec2.blockdevicemapping.BlockDeviceMapping()
block_device_map['/dev/xvda'] = dev_sda1

#Launch instances into VPC:
reservation = conn.run_instances(
                                max_count            = 1,
                                key_name             = 'AWS_CN_General',
                                image_id             = ami,
                                instance_type        = 't2.micro',
                                instance_profile_arn = 'arn:aws-cn:iam::153162420102:instance-profile/DevDaily',
                                user_data            = base64.b64encode(bootstrip_file_contents),
                                block_device_map     = block_device_map,
                                network_interfaces   = network_interface,
                                )


#Get the instance object:
instance = reservation.instances[0]

#Add Tag for the instances:
tags= {
        'Name': "DailyDev Machine Launch by " + USER ,
        'application':'sandbox',
        'environment':'dev',
        'role':'dev-testing',
        'owner': USER
        }
instance.add_tags(tags)

#Wait instances to ready for use: 
time.sleep(5)
instance.update()
while instance.state == "pending":
    print "Instance %s statue is %s, waiting instances state to become running.." % (instance.id, instance.state)
    time.sleep(5)
    instance.update()

#Check SSH Connection:
result = check_port(instance.public_dns_name, 22)
while result == 1:
    print "Checking If SSH ready for use.."
    time.sleep(5)
    result = check_port(instance.public_dns_name, 22)

#Bootstrip:
bootstrip(instance)

#Output instances info:
print "instance %s Ready! please login here:" % (instance.id)
print instance.public_dns_name

