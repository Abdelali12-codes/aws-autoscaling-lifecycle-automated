# aws-autoscaling-lifecycle-automated


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