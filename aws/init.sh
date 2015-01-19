#!/bin/bash - 
#===============================================================================
#
#          FILE: init.sh
# 
#         USAGE: ./init.sh {cn|global} [access_key] [secret_key]
# 
#   DESCRIPTION: Add aws credential to credential config file
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2015-01-15 12:36
#      REVISION:  ---
#===============================================================================


usage ()
{
    echo "This is script is used for initialize AWS credential profile"
    echo "Usage: $0 {cn|global} [access_key] [secret_key]"
    echo "   eg: Initialize AWS CN credential run:"
    echo "       $0 cn your_aws_access_key your_aws_secret_key" 
    
}	# ----------  end of function usage  ----------


init_env ()
{
    boto_version=$(python -c "import boto; print boto.Version" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "boto was already installed. version $boto_version"
        return
    fi
    os_relase=$(cat /etc/issue|head -n 1|awk '{print $1}')
    case $os_relase in
        CentOS|Amazon)
            rpm --quiet -q epel-release
            if [ $? -ne 0 ]; then
                sudo yum install epel-release -y
            fi
            sudo yum install python python-pip --enablerepo=epel -y
            sudo pip install boto
            ;;
        Fedora)
            sudo yum install python python-pip -y
            sudo pip install boto
            ;;
        Ubuntu|Debian)
            sudo apt-get update
            sudo apt-get install python python-pip -y
            sudo pip install boto
            ;;
        *)
            echo "This is a not supported OS"
            exit 1
            ;;
    esac
}	# ----------  end of function init_env  ----------

init_profile ()
{
cat >> ${HOME}/.aws/credentials <<EOF
[${profile}]
aws_access_key_id = ${access_key}
aws_secret_access_key = ${secret_key}

EOF
echo "Profile ${profile} was added to ${HOME}/.aws/credentials"

}	# ----------  end of function init_profile  ----------


check_args ()
{
   case $1 in
       cn)
           profile=$1
           ;;
       global)
           profile=$1
           ;;
       *)
           usage
           exit 1
           ;;
   esac

   # Check required files
   [ ! -d ${HOME}/.aws ] && mkdir ${HOME}/.aws
   [ ! -f ${HOME}/.aws/credentials ] && touch ${HOME}/.aws/credentials
   # Check if profile already exist
   grep -qs "\[${profile}\]" ${HOME}/.aws/credentials
   if [ $? -eq 0 ]; then
        echo "Error: Profile ${profile} already exist in ${HOME}/.aws/credentials. exiting..."
        exit 1
    fi

   if [ "$2" != "" ]; then
       access_key=$2
   else
       echo -n "Your AWS Access Key: "
       read access_key
   fi
   if [ `echo -n $access_key|wc -c` -ne 20 ]; then
       echo "Access Key not correct, exiting..."
       exit 1
   fi

   if [ "$3" != "" ]; then
       secret_key=$3
   else
       echo -n "Your AWS Secret Key: "
       read secret_key
   fi
   if [ `echo -n $secret_key|wc -c` -ne 40 ]; then
       echo "secret key not correct, exiting..."
       exit 1
   fi

}	# ----------  end of function check_args  ----------

# Install required software
init_env
# check argument
check_args "$@"
# Init profile
init_profile
