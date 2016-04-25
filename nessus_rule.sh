#!/usr/bin/bash

# CREATED BY JUSTIN TODD
# INSERTS IP ADDRESSES TO BE REJECT

# Syntax : accept|reject address/netmask
# reject 10.42.123.0/24

# You can also deny|allow certain ports :
# Forbid connecting to port 80 for 10.0.0.1 :
# reject 10.0.0.1:80
# Forbid connecting to ports 8000 - 10000 for any host in the 192.168.0.0/24 subnet :
# reject 192.168.0.0/24:8000-10000


# You can also deny|allow the use of certain plugin IDs :
# plugin-reject 10335
# plugin-accept 10000-40000

RULESFILE="/opt/nessus/etc/nessus/nessusd.rules"
SYNTAX=$1
LOG="nessus_rules.log"
IPADRESS="accept|reject address"
PORTS="# You can also deny|allow certain ports"
PLUGINS="deny|allow the use of certain plugin IDs"


# CHECK IF THERE IS A INPUT
if [[ "$1" == "" ]]; then
   echo "Invalid Input: [-h] help [-r] reject [-n] plugin-reject [-k] plugin-accept"
   exit 1
fi


# GET OPTIONS FROM COMMAND LINE [-h] help [-a] accept [-r] reject [-n] plugin-reject [-k] plugin-accept
while getopts ":h:a:r:n:k:p:" opt; do
  case $opt in
    h)
      echo "-h was triggered: $OPTARG" >&2
      echo "Syntax : accept|reject address/netmask ie. reject 10.42.123.0/24 . 10.42.123.1/24"
      echo "Reject connecting to port 80 for 10.0.0.1 ie. reject 10.0.0.1:80"
      echo "Forbid connecting to ports 8000 - 10000 ie. reject 192.168.0.0/24:8000-10000"
      echo "You can also deny/allow the use of certain plugin IDs ie. plugin-reject 10335 or plugin-accept 10000-40000"
      echo ""
      echo "Syntax: [-h] help [-a] accept [-r] reject [-n] plugin-reject [-k] plugin-accept"
      echo "[-a] [IP/CIDR]"
      echo "[-r] [IP/CIDR]"
      echo "[-p] [IP/CIDR:PORT] [IP/CIDR:PORT-PORT] " 
      echo "[-n] [plugin ID]"
      echo "[-k] [plugin ID]"
      ;;
    a)
      # CHECK FOR IMPROPER RULE SYNTAX CHAR ":"
      if [[ $OPTARG = *[':']* ]]; then
         echo "Invalid Parameter: [IP/CIDR]"
         exit 1
      else
      # CHECK FOR "/" IP/CIDR FORMAT
         if [[ $OPTARG = *['/']* ]]; then
            sed -i "/$IPADRESS/a accept $OPTARG" $RULESFILE
            echo "Added accept $OPTARG to $RULESFILE " >&2
            exit 0
         else
            echo "Missing Paremeter [IP/CIDR]"
            exit 1
         fi
      fi
      ;;
    r)
     # CHECK FOR IMPROPER RULE SYNTAX CHAR ":"
     if [[ $OPTARG = *[':']* ]]; then
         echo "Invalid Parameter: [IP/CIDR]"
         exit 1
      else
         # CHECK FOR "/" IP/CIDR FORMAT
         if [[ $OPTARG = *['/']* ]]; then
            echo "sed -i "/$IPADDRESS/a reject $OPTARG" $RULESFILE"
            echo "Added reject $OPTARG to $RULESFILE " >&2
            exit 0
         else
            echo "Missing Paremeter [IP/CIDR]"
            exit 1
         fi
      fi
      ;;
    n)
      # CHECK PLUGIN RULE FOR NON INTEGERS
      if [[ $OPTARG == ?(-)+([0-9]) ]]; then
	echo "Added plugin-reject $OPTARG to $RULESFILE" >&2
        sed -i "/$PLUGINS/a plugin-reject $OPTARG" $RULESFILE
        exit 0
      else 
	echo "Invalid Parameter: [PLUGIN-ID]. No other characters than a number/integer"
        exit 1
      fi
      ;;
    k)
      # CHECK PLUGIN RULE FOR NON INTEGERS 
      if [[ $OPTARG == ?(-)+([0-9]) ]]; then
        sed -i "/$PLUGINS/a plugin-accept $OPTARG" $RULESFILE
        echo "Added plugin-accept $OPTARG to $RULESFILE" >&2
        exit 0
      else
        echo "Invalid Parameter: [PLUGIN-ID]. No other characters than a number/integer"
        exit 1
      fi
      ;;
    p)
      # CHECK FOR ":" and "/"
      if [[ $OPTARG = *[':']* ]] && [[ $OPTARG = *['/']* ]]; then
            sed -i "/$PORTS/a reject $OPTARG" $RULESFILE
            echo "Added reject $OPTARG to $RULESFILE" >&2
            exit 0
         else
            echo "Missing Parameter: [IP/CIDR:PORT] [IP/CIDR:PORT-PORT]"
            exit 1
      fi
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
