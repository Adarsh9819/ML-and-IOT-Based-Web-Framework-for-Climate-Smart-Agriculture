import boto3
import json
import ast

def lambda_handler(event, context):
    # TODO implement
    runtime_client = boto3.client('runtime.sagemaker')
    endpoint_name = 'sagemaker-xgboost-2024-02-07-07-23-31-690'
    sample = '{},{},{},{},{},{},{}'.format(ast.literal_eval(event['body'])['x1'],
                                            ast.literal_eval(event['body'])['x2'],
                                            ast.literal_eval(event['body'])['x3'],
                                            ast.literal_eval(event['body'])['x4'],
                                            ast.literal_eval(event['body'])['x5'],
                                            ast.literal_eval(event['body'])['x6'],
                                            ast.literal_eval(event['body'])['x7'])
    
    response = runtime_client.invoke_endpoint(EndpointName=endpoint_name,
                                                ContentType='text/csv',
                                                Body=sample)
                                                
    result = int(float(response['Body'].read().decode('ascii')))
    
    
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': result})
    }
