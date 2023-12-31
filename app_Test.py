import subprocess
import boto3
import time
import os
from dotenv import load_dotenv
from functions import *
import visualization

# Load AWS credentials from credentials.env
load_dotenv("credentials.env")
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_session_token = os.environ["aws_session_token"]

# Define EC2 instance parameters
keyPairName = 'LOG8415E'
securityGroupName = 'LOG8415E_B2'

# Create an EC2 client
EC2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

WAITER = EC2.get_waiter('instance_status_ok')

# get vpc_id
vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
subnet = EC2.describe_subnets().get('Subnets', [{}])[0].get('SubnetId', '')

# create key pair and security group
print('Creating key pair...')
create_key_pair(EC2, keyPairName)
print('Creating security group...')
security_group = create_security_group(EC2, securityGroupName, vpc_id)


# ##############  Mysql setup   ##############
# Create 5 t2.micro instances
print("Creating mysql instance...")
instance_ids = create_t2micro_instances(EC2, keyPairName, security_group['GroupId'], subnet)
WAITER = EC2.get_waiter('instance_status_ok')
WAITER.wait(InstanceIds=instance_ids)
print("Mysql instances are running")

public_dns_mysql_standalone_instance = instance_ids[0]['Reservations'][0]['Instances'][0]['PublicDnsName']
public_dns_mysqlcluster_manager_instance = instance_ids[1]['Reservations'][0]['Instances'][0]['PublicDnsName']
private_ip_address_mysqlcluster_manager_instance = instance_ids[1]['Reservations'][0]['Instances'][0]['PrivateIpAddress']
public_dns_mysqlcluster_worker_instance_1 = instance_ids[2]['Reservations'][0]['Instances'][0]['PublicDnsName']
public_dns_mysqlcluster_worker_instance_2 = instance_ids[3]['Reservations'][0]['Instances'][0]['PublicDnsName']
public_dns_mysqlcluster_worker_instance_3 = instance_ids[4]['Reservations'][0]['Instances'][0]['PublicDnsName']
private_ip_address_mysqlcluster_worker_instance_1 = instance_ids[2]['Reservations'][0]['Instances'][0]['PrivateIpAddress']
private_ip_address_mysqlcluster_worker_instance_2 = instance_ids[3]['Reservations'][0]['Instances'][0]['PrivateIpAddress']
private_ip_address_mysqlcluster_worker_instance_3 = instance_ids[4]['Reservations'][0]['Instances'][0]['PrivateIpAddress']
os.system("chmod 700 " + keyPairName + ".pem")

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysqlcluster_manager_instance + " 'bash -s' < ./mysql_cluster_MasterNodeSetup_part2.sh "+
          public_dns_mysqlcluster_manager_instance + " " + public_dns_mysqlcluster_worker_instance_1 + " "+
          public_dns_mysqlcluster_worker_instance_2 + " " + public_dns_mysqlcluster_worker_instance_3)
time.sleep(30)

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysqlcluster_worker_instance_1 + " 'bash -s' < ./mysql_cluster_WorkerNodeSetup_part2.sh "+ public_dns_mysqlcluster_manager_instance)
time.sleep(30)

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysqlcluster_worker_instance_2 + " 'bash -s' < ./mysql_cluster_WorkerNodeSetup_part2.sh "+ public_dns_mysqlcluster_manager_instance)
time.sleep(30)

os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysqlcluster_worker_instance_3 + " 'bash -s' < ./mysql_cluster_WorkerNodeSetup_part2.sh "+ public_dns_mysqlcluster_manager_instance)
time.sleep(30)




# ##########################################
# ############## Benchmarking ##############

print("benchmarking for mysql standalone .....")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysql_standalone_instance + " 'bash -s' < ./sysbench.sh 2>> benchmarking/standalone_result.txt")
time.sleep(30)

print("Start benchmarking for mysql cluster ......")
os.system("ssh -o StrictHostKeyChecking=no -i " + keyPairName + ".pem ubuntu@" + public_dns_mysqlcluster_manager_instance + " 'bash -s' < ./sysbench.sh 2>> benchmarking/cluster_result.txt")
time.sleep(30)

print("Benchamarking completed...")



# ################################################
# ############## Delete everything  ##############
input("Press Enter to delete everything...")

# print("Terminating instance...")
# terminate_instance(EC2, instance_id)
# WAITER = EC2.get_waiter('instance_terminated')
# WAITER.wait(InstanceIds=[instance_id])
# print("Instance terminated")

print("Terminating instances...")
terminate_instances(EC2, instance_ids)
WAITER = EC2.get_waiter('instance_terminated')
WAITER.wait(InstanceIds=[instance_ids])
print("Instance terminated")

print("Deleting security group...")
delete_security_group(EC2, securityGroupName)

print("Deleting key pair...")
delete_key_pair(EC2, keyPairName)
