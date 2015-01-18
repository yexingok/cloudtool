#!/usr/bin/python

#Todo:
# Auto add/remove cloudwatch
# Auto config dynamic dns using aws global route53 ttl to 60 seconds 

import sys
import argparse
import os
import os.path
import socket
import time
import base64 
import boto.ec2

#Functions:

#Any Bootstrip?
def bootstrip(instance):
    print "Bootstrip instance.."
    time.sleep(1)

#Check port reachable
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

def main():
    parser = argparse.ArgumentParser(description='Edanz AWS CLI Tool - Launch Base AMI or your own specifiy AMI')
    parser.add_argument('-a', '--ami', required=True, help='The AMI you want to launched')
    parser.add_argument('-t', '--type', default='t2.micro', help='The instance type to launch (Default: %(default)s)')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='The file to provide user-data')
    parser.add_argument('-v', '--version', default=0.1, action='version', version='%(prog)s 0.1')
    parser.add_argument('--debug', type=int, default=0, choices=[0,1], help='--debug 1 enable debug mode')
    args = parser.parse_args()

    #Some Common Vars:
    USER = os.environ['USER']

    #Read user-data File: 
    bootstrip_file_contents = args.file.read()
    args.file.close()

    #Get time:
    time_display = time.strftime('%Y-%m-%d %H:%M:%S')

    #Connect to region with profile 'cn'
    if args.debug == 0 :
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn')
    else:
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn',debug=2)

    #Defined Tags:
    common_tags= {
            'Name': "DailyDev Resource Launch by " + USER + ' | ' + time_display ,
            'application': 'sandbox',
            'environment': 'dev',
            'role': 'dev-coding',
            'createtime': time_display,
            'cli_version': args.version,
            'owner': USER
            }
    ec2_special_tags = {
            'auto:start':'20 09 * * 1-5',
            'auto:stop':'30 19 * * *',
            }


    #Define the network interface will be used inside VPC:
    #TODO: auto select subnet.
    network_interface_config = boto.ec2.networkinterface.NetworkInterfaceSpecification(
            subnet_id                   = 'subnet-cc8b9bae',
            groups                      = ['sg-f59a8497'],
            description                 = "Created by Edanz CLI: ec2.py",
            delete_on_termination       = True,
            associate_public_ip_address = True
            )
    network_interface = boto.ec2.networkinterface.NetworkInterfaceCollection(network_interface_config)

    #Define the block device:
    #TODO: support more disks?
    dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType()
    dev_sda1.size = 20 
    dev_sda1.delete_on_termination = True
    dev_sda1.volume_type = 'gp2'

    block_device_map = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    block_device_map['/dev/xvda'] = dev_sda1

    #Launch instances into VPC:
    reservation = conn.run_instances(
                                    max_count            = 1,
                                    key_name             = 'AWS_CN_General',
                                    image_id             = args.ami,
                                    instance_type        = args.type,
                                    instance_profile_arn = 'arn:aws-cn:iam::153162420102:instance-profile/DevDaily',
                                    user_data            = base64.b64encode(bootstrip_file_contents),
                                    block_device_map     = block_device_map,
                                    network_interfaces   = network_interface,
                                    )


    #Get the instance object:
    instance = reservation.instances[0]

    #Add Tag for the instances:
    instance.add_tags(common_tags)
    instance.add_tags(ec2_special_tags)

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
        time.sleep(5)
        result = check_port(instance.public_dns_name, 22)

    #These tags need to add after instance ready:

    #Add Tag for networkinterface:
    network_interface = instance.interfaces[0]
    network_interface.add_tags(common_tags)

    #Add Tag for Block Device:
    volume_special_tags = {
            'mount-host':instance.id,
    }
    volume_id = instance.block_device_mapping['/dev/xvda'].volume_id
    conn.create_tags(volume_id,common_tags)
    conn.create_tags(volume_id,volume_special_tags)

    #Bootstrip:
    bootstrip(instance)

    #Output instances info:
    print "instance %s Ready! please login here:" % (instance.id)
    print instance.public_dns_name
        

#Functions end

if __name__ == "__main__":
    main()

