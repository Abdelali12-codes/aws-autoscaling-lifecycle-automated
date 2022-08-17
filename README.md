# aws-autoscaling-lifecycle-automated


## lambda code 

* create a s3 bucket
```
aws s3 mb s3://name-of-bucket
```
* zip the code
```
zip application.zip -r index.py
```
* copy your ziped code in it 
```
aws s3 cp application.zip s3://name-of-bucket
```

## SSM document schema

* version 1.2
```
{
   "schemaVersion":"1.2",
   "description":"A description of the SSM document.",
   "parameters":{
      "parameter 1":{
         "one or more parameter properties"
      },
      "parameter 2":{
         "one or more parameter properties"
      },
      "parameter 3":{
         "one or more parameter properties"
      }
   },
   "runtimeConfig":{
      "plugin 1":{
         "properties":[
            {
               "one or more plugin properties"
            }
         ]
      }
   }
}
```

* version 2.2
```
---
schemaVersion: "2.2"
description: A description of the document.
parameters:
  parameter 1:
    property 1: "value"
    property 2: "value"
  parameter 2:
    property 1: "value"
    property 2: "value"
mainSteps:
  - action: Plugin name
    name: A name for the step.
    inputs:
      input 1: "value"
      input 2: "value"
      input 3: "{{ parameter 1 }}"
      
```

* for the above schema action feature in the mainSteps, those plugins are already predefined, to see all plugins check the refences links

## References

* https://docs.aws.amazon.com/systems-manager/latest/userguide/document-schemas-features.html

### linux tar command documentation

* https://www.interserver.net/tips/kb/use-tar-command-linux-examples/

## bash commands

* https://stackoverflow.com/questions/24793069/what-does-do-in-bash
* https://devhints.io/bash
* https://linuxize.com/post/how-to-compare-strings-in-bash/
* https://www.thegeekstuff.com/2011/08/bash-history-expansion/
* https://stackoverflow.com/questions/47592506/what-does-exclamatory-mark-inside-curly-braces-when-using-variable-in-u

## bash indirection expansion
* https://riptutorial.com/bash/example/7567/parameter-indirection
* https://stackoverflow.com/questions/33068055/how-to-handle-errors-with-boto3

## example of the event that eventbridge will send to lambda

```
{
  "version": "0",
  "id": "12345678-1234-1234-1234-123456789012",
  "detail-type": "EC2 Instance-launch Lifecycle Action",
  "source": "aws.autoscaling",
  "account": "123456789012",
  "time": "yyyy-mm-ddThh:mm:ssZ",
  "region": "us-west-2",
  "resources": [
    "auto-scaling-group-arn"
  ],
  "detail": { 
    "LifecycleActionToken": "87654321-4321-4321-4321-210987654321", 
    "AutoScalingGroupName": "my-asg", 
    "LifecycleHookName": "my-lifecycle-hook", 
    "EC2InstanceId": "i-1234567890abcdef0", 
    "LifecycleTransition": "autoscaling:EC2_INSTANCE_LAUNCHING",
    "NotificationMetadata": "additional-info"
  } 
}

```

## create cloudformation stack using cli

```
 aws cloudformation create-stack \
  --stack-name myteststack \
  --template-body file:///home/testuser/mytemplate.json \
  --parameters ParameterKey=Parm1,ParameterValue=test1 ParameterKey=Parm2,ParameterValue=test2
```
## to mount efs to an aws lambda

* PYTHONPATH	/mnt/efs