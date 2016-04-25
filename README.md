Inserts IP/PORTS exclusions into /opt/nessus/etc/nessus/nessusd.rules for nessus

Example:

      Syntax : accept|reject address/netmask ie. reject 10.42.123.0/24 . 10.42.123.1/24"
      Reject connecting to port 80 for 10.0.0.1 ie. reject 10.0.0.1:80"
      Forbid connecting to ports 8000 - 10000 ie. reject 192.168.0.0/24:8000-10000"
      You can also deny/allow the use of certain plugin IDs ie. plugin-reject 10335 or plugin-accept 10000-40000"
      
            Syntax: [-h] help [-a] accept [-r] reject [-n] plugin-reject [-k] plugin-accept"
            [-a] [IP/CIDR]
            [-r] [IP/CIDR]
            [-p] [IP/CIDR:PORT] [IP/CIDR:PORT-PORT] 
            [-n] [plugin ID]
            [-k] [plugin ID]

./nessus_rule.sh -a 192.168.1.1/24
./nessus_rule.sh -r 192.168.1.2/24
./nessus_rule.sh -p 192.168.1.3/24:80 or range ./nessus_rule.sh -p 192.168.1.3/24:1000-2000
./nessus_rule.sh -n 100

