from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.examples.pyretic_switch import *

# insert the name of the module and policy you want to import
#from pyretic.examples.<....> import <....>

#policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]
#policy_file = "%s/pyretic/pyretic/examples/firewall-policies_small.csv" % os.environ[ 'HOME' ]

def main():
    # Copy the code you used to read firewall-policies.csv last week


    # start with a policy that doesn't match any packets
    not_allowed = match(srcmac=MAC("00:00:00:00:00:01"),dstmac=MAC("00:00:00:00:00:02")) | match(srcmac=MAC("00:00:00:00:00:02"),dstmac=MAC("00:00:00:00:00:01"))    # and add traff$
    #for <each pair of MAC address in firewall-policies.csv>:
    #    not_allowed = not_allowed + ( <traffic going in one direction> ) + ( <traffic going in the other direction> )


    # express allowed traffic in terms of not_allowed - hint use '~'
    allowed = ~not_allowed

    # and only send allowed traffic to the mac learning (act_like_switch) logic
    return allowed >> ActLikeSwitch()