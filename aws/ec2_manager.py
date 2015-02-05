#!/usr/bin/python

import os
import argparse
import time
import boto.ec2

#Functions:

def ec2_list(ec2_connection, user):
    print "List ec2 for user %s" % user
    instances = ec2_connection.get_only_instances()
    for instance in instances:
        try: 
            if instance.tags.get('owner') == user:
                print 'ID: %s\tState: %s\tOwner: %s\tCreated: %s\tPublic_DNS: %s\tName:"%s"' % (instance.id, instance.state, instance.tags.get('owner'), instance.tags.get('createtime'), instance.public_dns_name, instance.tags.get('Name'))
        except Exception as e:
            print '%s' % (e.message)

def ec2_start(ec2_connection, instance_id):
    print "Start ec2: %s" % instance_id
    try: 
        ec2_connection.start_instances(instance_id)
        print "You can use -l to check instance state"
    except Exception as e:
        print '%s' % (e.message)

def ec2_stop(ec2_connection, instance_id):
    print "Stop ec2: %s" % instance_id
    try: 
        ec2_connection.stop_instances(instance_id)
        print "You can use -l to check instance state"
    except Exception as e:
        print '%s' % (e.message)

def ec2_reboot(ec2_connection, instance_id):
    print "Reboot ec2: %s" % instance_id
    try: 
        ec2_connection.reboot_instances(instance_id)
        print "You can use -l to check instance state"
    except Exception as e:
        print '%s' % (e.message)


def ec2_terminate(ec2_connection, instance_id):
    print "Terminate ec2: %s" % instance_id
    try: 
        ec2_connection.terminate_instances(instance_id)
        print "You can use -l to check instance state"
    except Exception as e:
        print '%s' % (e.message)

def main():
    parser = argparse.ArgumentParser(description='Edanz AWS CLI Tool - Manage your own ec2 instances from CLI')
    parser.add_argument('-l', '--list', action='store_true', help='List current user\'s ec2 resources. If -u specified, will list users that -u specified')
    parser.add_argument('-u', '--user', default=os.environ['USER'], help='Specified a user, combined with -l')
    parser.add_argument('--start', metavar='instance_id', help='Start the Specified ec2 instances list')
    parser.add_argument('--stop', metavar='instance_id', help='Stop the Specified ec2 instances list')
    parser.add_argument('--reboot', metavar='instance_id', help='Reboot the ec2 instances list')
    parser.add_argument('--terminate', metavar='instance_id', help='Terminate the Specified ec2 instance, (use with caution! all data will be removed from the instances)')
    parser.add_argument('-v', '--version', default=0.1, action='version', version='%(prog)s 0.1')
    parser.add_argument('--debug', type=int, default=0, choices=[0,1], help='--debug 1 enable debug mode')
    args = parser.parse_args()


    #Connect to region with profile 'cn'
    if args.debug == 0:
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn')
    else:
        conn = boto.ec2.connect_to_region('cn-north-1',profile_name='cn',debug=2)
        print args

    if args.list :
        ec2_list(conn, args.user)
    else:
        if args.start != None :
            ec2_start(conn, args.start)
        if args.stop != None :
            ec2_stop(conn, args.stop)
        if args.reboot != None :
            ec2_reboot(conn, args.reboot)
        if args.terminate != None :
            ec2_terminate(conn, args.terminate)

#Functions end

if __name__ == "__main__":
    main()

