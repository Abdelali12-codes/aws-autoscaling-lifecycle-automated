import boto3
import logging
import os.path


ssm = boto3.client("ssm")

#the arguments of this method is the name of paramaters
# get_ssm_parameters("/db/dev/name")
def get_ssm_parameters(*args):
    
    
    if len(args) > 0:
        params = [x for x in args]
        
        try:
            parameters = ssm.get_parameters(Names=params, WithDecryption=True)
            
            if len(parameters['Parameters']) > 0:
                for param in parameters['Parameters']:
                   print("{0}={1}".format(param['Name'],param['Value']))
                return parameters['Parameters']
        except Exception as ex:
            print(ex)
           
    else:
        print("please provide your parmaters")
        
        
# the arguments of this method is the name of documents  
# example list_ssm_document("documenname")
def list_ssm_document(*args):
    
    
    if len(args) > 0:
        documents = [{'key':'Name' , 'value': doc}  for doc in args]
        
        try:
            respond = ssm.list_documents(DocumentFilterList=documents)
            
            if len(respond['DocumentIdentifiers']) > 0:
              return respond
        except Exception as ex:
            print(ex)
          
    else :
        print("please provide your documents nameq")
        
def send_ssm_document(**kargs):
    
    if len(kargs) > 0:
    # kargs is a dic
        try:
            
            respond = ssm.send_command(
                InstanceIds= kargs['InstanceIds'],
                DocumentName= kargs['DocumentName'],
                NotificationConfig={
                'NotificationArn': kargs['SNSARN'],
                'NotificationEvents': [
                    'All',
                ],
                'NotificationType': 'Command'
                },
            )
            
            
        except Exception as ex:
            print(ex)
            
def send_ssm_create_document(**kargs):
    
    
    if len(kargs) > 0:
        
        path= kargs['path']
        documentname= kargs['name']
        
        try:
            # TODO: write code...
            if os.path.exists(path):
                respond = ssm.create_document(
                    Content= path,
                    Name = documentname ,
                    DocumentType='Command'
                )
            else:
                print(f"{path} file does not exist")
            
        except Exception as e:
            print(e)
            
get_ssm_parameters("/my-db/dev/password")