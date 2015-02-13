cloudtool
=========

Introduction:
=============

aws/ - all tools for manage aws CLI
aws/init.sh     script for install basic aws sdk and setup local SDK credential environment.
aws/ec2_launch.py   script for launching ec2 resources.
aws/ec2_manager.py  scruot for managing ec2 resources 
aws/ec2_operator.py script for auto start/stop instances based on tag auto:start/auto:stop.
aws/ami_create.py  script for creating ami
aws/ami_manager.py  script for managing ami 

Get started:
==============

* Clone this repo
* Get your AWS access key credential from ops team.
* Setup dependence
  * If you are on ubuntu or fedore, simply run the init.sh to setup dependence:
      * cd aws
      * ./init.sh cn your_access_key_id  your_access_key
  * If you are on other distribution, you need to use your package manage tool to install the following package:
      * python 
      * python-pip
      * boot, can be installed with: pip install boto 
* You can list our AMI using:
  * ./ami_manager.py -l -u ops this command will list all the AMI our ops team prepared for you, please select the AMI end with 'all users'
* You can launch instances using:
  * ./ec2_launch.py --ami the_ami_id 
* You can use -h to get help for each command.

Enjoy!

If you have any questions, please feel free to dicuss with us and  bring up a support ticket.
Thanks!
