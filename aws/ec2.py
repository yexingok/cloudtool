#!/usr/bin/python

import os.path
import boto.ec2

#Some Common Vars:
SCRIPT_NAME = os.path.basename(__file__)
USER = 'yexing'

#Define:
#centos7 HVM:
ami = 'ami-ce46d4f7'

conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn')

#Define the network interface used for launching in VPC, confusing sdk..
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
block_device_map['/dev/sda1'] = dev_sda1

#Launch instances into VPC:
reservation = conn.run_instances(
                                max_count            = 1,
                                key_name             = 'AWS_CN_General',
                                image_id             = ami,
                                instance_type        = 't2.micro',
                                instance_profile_arn = 'arn:aws-cn:iam::153162420102:role/DevDaily',
                                user_data            = '',
                                block_device_map     = block_device_map,
                                network_interfaces   = network_interface,
                                )


#Get the instance:
instance_a = reservation[0].instances
instance = instance_a[0]

#Add Tag for the instances:
tags= {
        'Name': "DailyDev Machine Launch by " + USER ,
        'application':'no',
        'environment':'dev',
        'role':'dev-testing',
        'owner': USER
        }
instance.add_tags(tags)

#Wait instances to ready for use: 
instance.update()
while instance.state == "pending":
    print "Instance %s statue is %s, waiting instances state to become running.." % (instance.id, instance.state)
    time.sleep(5)
    instance.update()

#Bootstrip:

#Output instances info:
print "instance %s Ready! please login here: %s" % (instances.id, instances.public_dns_name)

