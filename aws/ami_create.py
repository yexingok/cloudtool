#!/usr/bin/python

#Todo:

import os
import time
import argparse
import boto.ec2

#Functions:

def main():
    parser = argparse.ArgumentParser(description='Edanz AWS Create Tool - Make an AMI from a instance')
    parser.add_argument('instance_id', action='store', help='The instance id to make the AMI')
    parser.add_argument('-r', '--reboot', action='store_true', help='Reboot instance when make AMI')
    parser.add_argument('-n', '--name', metavar="'AMI Name String'", help='Specified AMI name, if not specified, it will generate automatically')
    parser.add_argument('-v', '--version', default=0.1, action='version', version='%(prog)s 0.1')
    parser.add_argument('--debug', type=int, default=0, choices=[0,1], help='--debug 1 enable debug mode')
    args = parser.parse_args()

    #Some Common Vars:
    USER = os.environ['USER']

    #Connect to region with profile 'cn'
    if args.debug == 0 :
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn')
    else:
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn',debug=2)

    instance_ids = []
    instance_ids.append(args.instance_id)
    try:
        instances = conn.get_only_instances(instance_ids)
        instance = instances[0]
    except Exception as e:
        print '%s' % e.message
 
    #Get time:
    current_time = time.localtime()
    time_display = time.strftime('%Y-%m-%d %H:%M:%S',current_time)
    time_short_display = time.strftime('%Y%m%d-%H%M%S',current_time)

    # Rebbot instance or not
    if args.reboot :
        noreboot = False
    else:
        noreboot = True

    # If specified Name
    if args.name != None:
        tag_name = args.name
    else:
        instance_name = instance.tags['Name'] if 'Name' in instance.tags else instance.id
        tag_name = 'snapshot for ' + instance_name + " at " + time_display

    #Defined Tags:
    common_tags= {
            'Name': tag_name ,
            'application': 'sandbox',
            'environment': 'dev',
            'role': 'dev-coding',
            'createtime': time_display,
            'cli_version': args.version,
            'owner': USER
            }

    # Tags from origin instance
    common_tags['application'] = instance.tags['application'] if 'application' in instance.tags else 'sandbox'
    common_tags['environment'] = instance.tags['environment'] if 'environment' in instance.tags else 'dev'
    common_tags['role'] = instance.tags['role'] if 'role' in instance.tags else 'dev-coding'
    common_tags['owner'] = instance.tags['owner'] if 'owner' in instance.tags else USER

    # AMI Name
    ami_name = "snapshot for " + instance.id + " at " + time_short_display

    # Create AMI
    print "Creating AMI for instance '%s': %s" % (instance.tags['Name'] if 'Name' in instance.tags else instance.id,\
            instance.id if 'Name' in instance.tags else None)
    try:
        image_id = instance.create_image(ami_name,no_reboot=noreboot,dry_run=False)
        time.sleep(2)
        print "Taging AMI " + image_id
        image = conn.get_image(image_id)
        image.add_tags(common_tags)
        print "AMI was created, it might take serveral minutes to finish"
    except Exception as e:
        print e.message

#Functions end

if __name__ == "__main__":
    main()

