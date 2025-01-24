from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError

class S3Manager:

    def __init__(self, region_name='sa-east-1'):
        self.client = boto3.client('s3', region_name=region_name)

    def upload_file_obj(self, file_obj: any,  bucket_name: str, object_name: str) -> Dict[str, Any]:
        try:
            return self.client.upload_fileobj(
                file_obj,
                bucket_name,
                object_name
            )
        except ClientError as exception:
            raise Exception(f'Failed uploading file to {bucket_name}/{object_name}: {str(exception)}')

    def get_object(self, bucket_name: str, object_name: str) -> str:
        try:
            
            object_response = self.client.get_object(
                Bucket=bucket_name,
                Key=object_name
            )

            return object_response

        except ClientError as exception:
            raise Exception(f'Failed to get object {object_name} from bucket {bucket_name}: {str(exception)}')
    
    def list_objects(self, bucket_name: str, prefix: str) -> Dict[str, Any]:

        try:
            return self.client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix
            )
        except ClientError as exception:
            raise Exception(f'Failed to list objects: {str(exception)}')
    
    def delete_object(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        try:
            return self.client.delete_object(
                Bucket=bucket_name,
                Key=object_name
            )
        except ClientError as exception:
            raise Exception(f'Failed to delete object {bucket_name}/{object_name}: {str(exception)}')
        

# USAGE EXAMPLE
s3_manager = S3Manager(region_name='sa-east-1')
        
# Uploading a file
with open('/path/to/file/test.py', 'rb') as file:
    s3_manager.upload_file_obj(file, 'test-bucket-011124', object_name='resources/test.py')
        
# Get Object
s3_object = s3_manager.get_object('my-bucket', 'file.txt')
        
# Listing bucket objects
objetos = s3_manager.list_objects('my-bucket')
        
# Delete a object
s3_manager.delete_object('my-bucket', 'file.txt')