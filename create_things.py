import boto3
import json

def createThing(thingName):
    global thingClient

    thingArn = ''
    thingId = ''
    defaultPolicyName = 'IoTPolicy'
    thingGroupName = 'my_things'
    thingGroupArn = 'arn:aws:iot:us-east-1:860795982569:thinggroup/my_things'

    thingResponse = thingClient.create_thing(
        thingName = thingName
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data: 
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']

    certResponse = thingClient.create_keys_and_certificate(
        setAsActive = True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data: 
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']
                            
    with open('certs/' + thingName + '_public.key', 'w') as outfile:
        outfile.write(PublicKey)
    with open('certs/' + thingName + '_private.key', 'w') as outfile:
        outfile.write(PrivateKey)
    with open('certs/' + thingName + '_cert.pem', 'w') as outfile:
        outfile.write(certificatePem)
    with open('certs/' + thingName + '_cert_id.txt', 'w') as outfile:
        outfile.write(certificateId)

    response = thingClient.attach_policy(
        policyName = defaultPolicyName,
        target = certificateArn
    )
    response = thingClient.attach_thing_principal(
        thingName = thingName,
        principal = certificateArn
    )
    response = thingClient.add_thing_to_thing_group(
        thingGroupName = thingGroupName,
        thingGroupArn = thingGroupArn,
        thingName = thingName,
        thingArn = thingArn,
        overrideDynamicGroups = False
    )

thingClient = boto3.client('iot')
for thing_number in range(1, 6):
    createThing(thingName = 'my_thing_' + ('%03d' % thing_number))