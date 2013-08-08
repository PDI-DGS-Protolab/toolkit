__author__ = 'mac'

import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance

from config import REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY, INSTANCE_ID, REPO, KEY_PAIR

def get_instance_by_id(instance_id):
    conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    reservations = conn.get_all_instances([instance_id])

    if len(reservations) != 1:
        return None

    reservation = reservations[0]

    instances = reservation.instances

    if len(instances) == 0:
        return None

    return instances[0]

def execute_script(instance, key_pair, script):
    ssh_client = sshclient_from_instance(instance, key_pair, user_name='ec2-user')

    status, stdin, stderr = ssh_client.run(script)

    print status
    print stdin
    print stderr


############### MAIN ##################

instance = get_instance_by_id(INSTANCE_ID)
execute_script(instance, KEY_PAIR, "update_code {0}".format(REPO))


