# INSTANCE

def create_instance(client, keyPair, securityGroupId, subnetId, instance_type, instance_name, setupfile_name):
    print('Creating 1 instance of ...'+ instance_type)
    response = client.run_instances(

        ImageId='ami-08c40ec9ead489470',
        InstanceType=instance_type,
        KeyName=keyPair,
        UserData=open(setupfile_name).read(),
        SubnetId=subnetId,
        SecurityGroupIds=[
            securityGroupId,
        ],
        MaxCount=1,
        MinCount=1,
        Monitoring={   
            'Enabled': True
        },
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },
                ]
            },
        ],
    )
    return response["Instances"][0]["InstanceId"]



def terminate_instance(client, instanceId):
    print('terminating instance:')
    print(instanceId)
    client.terminate_instances(InstanceIds=([instanceId]))


# This function terminates the running instances ".
def terminate_instances(client, instanceIds):
    print('terminating cluster of instances:')
    print(instanceIds)
    client.terminate_instances(InstanceIds=(instanceIds))

    
# KEY PAIR

def create_key_pair(ec2_client, key_pair_name):
    try:
        key_pair = ec2_client.create_key_pair(KeyName=key_pair_name)
        # Save the PEM file locally
        with open(f'{key_pair_name}.pem', 'w') as pem_file:
            pem_file.write(key_pair['KeyMaterial'])
        print(f'Key pair {key_pair_name} created and PEM file saved as {key_pair_name}.pem')
    except ec2_client.exceptions.ClientError as e:
        if 'KeyPair' in str(e):
            print(f'Key pair {key_pair_name} already exists.')
        else:
            raise
    
    return key_pair['KeyName']

def delete_key_pair(ec2_client,  key_pair_name):

    try:
        ec2_client.delete_key_pair(KeyName=key_pair_name)
        print(f'Deleted key pair: {key_pair_name}')
    except ec2_client.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print(f'Key pair {key_pair_name} does not exist.')
        else:
            raise

# SECURITY GROUP

def create_security_group(ec2_client, security_group_name, vpc_id):
    try:
        security_group = ec2_client.create_security_group(
            Description='LOG8415 Security Group',
            GroupName=security_group_name,
            VpcId=vpc_id
        )

        response = ec2_client.describe_security_groups(
        GroupNames=[security_group_name]
        )
        security_group_id = response['SecurityGroups'][0]['GroupId']

        # Add inbound rules 
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,  # SSH port
                    'ToPort': 22,    # SSH port
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 8080,  
                    'ToPort': 8080,    
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] #"Gatekeeper server port" 
                }, 
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 8080,  
                    'ToPort': 8081,    
                    'IpRanges': [{'CidrIp': '172.31.0.0/16'}] #"Proxy server port" 
                },
                {
                    'IpProtocol': 'icmp',
                    'FromPort': -1,  
                    'ToPort': -1,    
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}] #"Proxy server port" 
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3306,  
                    'ToPort': 3306,    
                    'IpRanges': [{'CidrIp': '172.31.0.0/16'}] #"MySQL port" 
                },          
            ]
        )

    except ec2_client.exceptions.ClientError as e:
        if 'already exists' in str(e):
            print(f'Security group {security_group_name} already exists.')
        else:
            raise

    return security_group

def delete_security_group(ec2_client, security_group_name):
    try:
        ec2_client.delete_security_group(GroupName=security_group_name)
        print(f'Deleted security group: {security_group_name}')
    except ec2_client.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print(f'Security group {security_group_name} does not exist.')
        else:
            raise
