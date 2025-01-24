import boto3
from botocore.exceptions import ClientError

class CloudWatchLogCreator:
    
    def __init__(self, region_name='sa-east-1'):
        self.region_name = region_name
        self.client = boto3.client('cloudwatch', region_name=region_name)
    
    def create_log_group(self, log_group_name: str, retention_in_days: int) -> None:
        """Cria um grupo de logs se não existir."""
        try:
            self.client.create_log_group(logGroupName=log_group_name)
            self.logger.info(f'Log group {log_group_name} created.')

            if retention_in_days > 0:
                self.client.put_retention_policy(
                    logGroupName=log_group_name,
                    retentionInDays=retention_in_days
                )
                print(f'Retention policy set to {retention_in_days} days for log group {log_group_name}.')

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f'Log group already exists: {log_group_name}: {str(e)}')
            else:
                raise Exception(f'Failed to create log group: {str(e)}')

    def create_log_stream(self, log_group_name: str, log_stream_name: str) -> None:
        """Cria um stream de logs se não existir."""
        try:
            self.client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            print(f'Log stream {log_stream_name} created.')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print(f'Log stream already exists: {log_stream_name}: {str(e)}')
            else:
                raise Exception(f'Failed to create log stream: {str(e)}')

# USAGE EXAMPLE

cw_log_creator = CloudWatchLogCreator(region_name='sa-east-1')

cw_log_creator.create_log_group('My-log-group', 7)
cw_log_creator.create_log_stream('My-log-group', 'log-stream')
