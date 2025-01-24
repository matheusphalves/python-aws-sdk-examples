import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
import json

class SecretsManager:

    def __init__(self, region_name='sa-east-1'):
        self.region_name = region_name
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, name: str) -> Dict[str, Any]:
        """Recupera o valor de um segredo armazenado no AWS Secrets Manager."""
        try:
        
            response = self.client.get_secret_value(SecretId=name)
            secret_string = response.get('SecretString', '{}')
            secret_value = json.loads(secret_string)
            return secret_value
        
        except ClientError as e:
            raise Exception(f'Error recovering secret: {name}: {e}')
        

# USAGE EXAMPLE
secret_name = '/my/secret'

secrets_manager = SecretsManager()

try:
    secret = secrets_manager.get_secret(secret_name)
    print(f"Secret value: {secret}")

except Exception as e:
    print(f"Failed recovering secret {secret_name}: {e}")