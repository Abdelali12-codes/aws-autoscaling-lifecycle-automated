import boto3
import logging
import os.path
import os
import time
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



EC2_Key= "EC2InstanceId"
ASG_Key = "AutoScalingGroupName"
Hook_key= "LifecycleHookName"
Document_Name= os.environ.get("DOCUMENT_NAME")

ssm = boto3.client("ssm")


def check_response(response):
    try:
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except KeyError:
        return False   
        
    
        
# list document based on the document name
def list_document():
    document_filter_parameters = {'key': 'Name', 'value': Document_Name}
    response = ssm.list_documents(
        DocumentFilterList=[ document_filter_parameters ]
    )
    return response
        

# check wether a document exist or note
def check_document_status():
     # If the document already exists, it will not create it.
    try:
        response = list_document()
        if check_response(response):
            logger.info("Documents list: %s", response)
            if any(response['DocumentIdentifiers']):
                logger.info("Documents exists: %s", response)
                return True
            else:
                return False
        else:
            logger.error("Documents' list error: %s", response)
            return False
    except Exception as e:
        logger.error("Document error: %s", str(e))
        return None
        
# if the document exists then send the command to the target instance with the instance ID        
def send_command(instance_id):
    # Until the document is not ready, waits in accordance to a backoff mechanism.
    while True:
        timewait = 1
        response = check_document_status()
        if any(response["DocumentIdentifiers"]):
            break
        time.sleep(timewait)
        timewait += timewait
    try:
        response = ssm.send_command(
            InstanceIds = [ instance_id ],
            DocumentName = Document_Name,
            TimeoutSeconds = 120
            )
        if check_response(response):
            logger.info("Command sent: %s", response)
            return response['Command']['CommandId']
        else:
            logger.error("Command could not be sent: %s", response)
            return None
    except Exception as e:
        logger.error("Command could not be sent: %s", str(e))
        return None
        
# check the status of the command running on the instance
# this method is the one that will give us an idea wether to abandon the termination of instance or not
# that is why this method enable us to keep tracking the status of the command
def check_command_status(command_id, instance_id):
    timewait = 1
    while True:
        try:
            response_iterator = ssm.list_command_invocations(
                CommandId = command_id,
                InstanceId = instance_id,
                Details=False
                )
            if check_response(response_iterator):
                response_iterator_status = response_iterator['CommandInvocations'][0]['Status']
                if response_iterator_status != 'Pending':
                    if response_iterator_status == 'InProgress' or response_iterator_status == 'Success':
                        logging.info( "Status: %s", response_iterator_status)
                        return True
                    else:
                        logging.error("ERROR: status: %s", response_iterator)
                        return False
            time.sleep(timewait)
            timewait += timewait
        except Exception as e:
            logger.error("Lifecycle hook abandon could not be executed: %s", str(e))
            return None
        
        
# this method will be called when the event arrive because all the arguments of the function will
# be retrieved from the event['detail']
def abandon_lifecycle(life_cycle_hook, auto_scaling_group, instance_id):
    asg_client = boto3.client('autoscaling')
    try:
        response = asg_client.complete_lifecycle_action(
            LifecycleHookName=life_cycle_hook,
            AutoScalingGroupName=auto_scaling_group,
            LifecycleActionResult='CONTINUE',
            InstanceId=instance_id
            )
        if check_response(response):
            logger.info("Lifecycle hook abandoned correctly: %s", response)
        else:
            logger.error("Lifecycle hook could not be abandoned: %s", response)
    except Exception as e:
        logger.error("Lifecycle hook abandon could not be executed: %s", str(e))
        return None
        


def handler(event, context):
    try:
        logger.info(json.dumps(event))
        message = event['detail']
        if Hook_key in message and ASG_Key in message:
            life_cycle_hook = message[Hook_key]
            auto_scaling_group = message[ASG_Key]
            instance_id = message[EC2_Key]
            if check_document_status():
                command_id = send_command(instance_id)
                if command_id != None:
                    if check_command_status(command_id, instance_id):
                        logger.info("Lambda executed correctly")
                    else:
                        abandon_lifecycle(life_cycle_hook, auto_scaling_group, instance_id)
                else:
                    abandon_lifecycle(life_cycle_hook, auto_scaling_group, instance_id)
            else:
                abandon_lifecycle(life_cycle_hook, auto_scaling_group, instance_id)
        else:
            logger.error("No valid JSON message: %s", json.dumps(message))
    except Exception as e:
        logger.error("Error: %s", str(e))