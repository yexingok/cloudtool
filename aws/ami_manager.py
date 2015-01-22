#!/usr/bin/python

#Todo:

import os
import argparse
import boto.ec2

#Functions:

#List user amis
def list_user_amis(ec2_connection, user):
    print "List AMIs for user %s" % user
    images = ec2_connection.get_all_images(owners='self')
    for image in images:
        try:
            if image.tags.get('owner') == user:
                print 'ID: %s\tName:"%s"\tOwner:%s\tCreated:%s' % (image.id, image.name, image.tags.get('owner'), image.tags.get('createtime'))
        except Exception as e:
            print '%s' % (e.message)

# Delete AMIs
def delete_amis(ec2_connection, image_ids):
    for image_id in image_ids:
        try:
            image = ec2_connection.get_image(image_id)
            print 'Deleting AMI: %s\t Name: "%s"\t Owner: %s\t' % (image.id, image.name, image.tags.get('owner'))
            image.deregister(dry_run=True)
        except Exception as e:
            print '%s' % (e.message)

def main():
    parser = argparse.ArgumentParser(description='Edanz AWS CLI Tool - Manage AWS AMIs')
    parser.add_argument('-l', '--list', action='store_true', help='List current user\'s AMIs. If -u specified, will list users that -u specified')
    parser.add_argument('-u', '--user', help='Specified a user, combined with -l')
    parser.add_argument('-d', '--delete', metavar="AMI_id", nargs='+', help='Specified AMI ids to delete')
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

    #List AMIs
    if args.list :
        if args.user == None:
            list_user_amis(conn, USER)
        else:
            list_user_amis(conn, args.user)

    # Delete AMIs
    if args.delete != None:
        delete_amis(conn, args.delete)

#Functions end

if __name__ == "__main__":
    main()

