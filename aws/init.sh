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

init_profile ()
{
    [ ! -d ${HOME}/.aws ] && mkdir ${HOME}/.aws
    [ ! -f ${HOME}/.aws/credentials ] && touch ${HOME}/.aws/credentials
    grep -qs "\[${profile}\]" ${HOME}/.aws/credentials
    if [ $? -ne 0 ]; then
        cat >> ${HOME}/.aws/credentials <<EOF
[${profile}]
aws_access_key_id = ${access_key}
aws_secret_access_key = ${secret_key}

EOF
        echo "Profile ${profile} was added to ${HOME}/.aws/credentials"
    else
        echo "Profile ${profile} already exist in ${HOME}/.aws/credentials"
        exit
    fi
    
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
           exit
           ;;
   esac

   if [ "$2" != "" ]; then
       access_key=$2
   else
       echo -n "Your AWS Access Key: "
       read access_key
       if [ `echo -n $access_key|wc -c` -ne 20 ]; then
           echo "Access Key not correct, exiting..."
           exit
       fi
   fi

   if [ "$3" != "" ]; then
       secret_key=$3
   else
       echo -n "Your AWS Secret Key: "
       read secret_key
       if [ `echo -n $secret_key|wc -c` -ne 40 ]; then
           echo "Secret Key not correct, exiting..."
           exit
       fi
   fi

}	# ----------  end of function check_args  ----------

# check argument
check_args "$@"
# Init profile
init_profile
