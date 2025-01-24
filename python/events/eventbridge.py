import boto3
from botocore.exceptions import ClientError


class EventBridgeManager:
    def __init__(self, region_name='sa-east-1'):
        self.client = boto3.client('events', region_name=region_name)

    def get_scheduler_rule_by_name(self, rule_name: str) -> dict:
        try:
        
            return self.client.describe_rule(Name=rule_name)
        
        except ClientError as exception:
            if exception.response['Error']['Code'] == 'ResourceNotFoundException':
                return None
            else:
                raise Exception(f"Failed to retrieve scheduler rule", exception)
            
    def get_targets_for_rule(self, rule_name):
        try:
            response = self.client.list_targets_by_rule(Rule=rule_name)
            return response.get('Targets', [])
        
        except ClientError as exception:
            if exception.response['Error']['Code'] == 'ResourceNotFoundException':
                pass
            else:
                raise Exception(f'Failed to get targets for rule: {rule_name}', exception)
        return []
            
    def update_targets(self, rule_name: str, targets: list):

        try:
            return self.client.put_targets(
                Rule=rule_name,
                Targets=targets
            )
        except ClientError as exception:
            raise Exception(f'Failed to put targets for rule: {rule_name}', exception)
        
    def update_rule(self, rule_name: str, schedule_expression: str, state: str) -> dict:
        try:
        
            return self.client.put_rule(
                Name=rule_name,
                ScheduleExpression=schedule_expression,
                State=state
            )
        
        except ClientError as exception:
            raise Exception(f'Failed to update rule for rule: {rule_name}', exception)
        
# USAGE EXAMPLE
region = 'us-west-2'  
eventbridge_manager = EventBridgeManager(region)

rule_name = 'my-scheduled-rule'

rule = eventbridge_manager.get_scheduler_rule_by_name(rule_name)
if rule:
    print(f"Rule found: {rule}")
else:
    print(f"Rule {rule_name} not found.")


targets = eventbridge_manager.get_targets_for_rule(rule_name)
if targets:
    print(f"Targets for {rule_name}: {targets}")
else:
    print(f"No targets found for rule {rule_name}.")


new_schedule_expression = 'rate(5 minutes)' 
new_state = 'ENABLED'
updated_rule = eventbridge_manager.update_rule(rule_name, new_schedule_expression, new_state)
print(f"Updated rule: {updated_rule}")


new_targets = [
    {
        'Id': 'new-target-1',
        'Arn': 'arn:aws:lambda:us-west-2:123456789012:function:my-lambda-function',
        'Input': '{"key": "value"}'
    },
    {
        'Id': 'new-target-2',
        'Arn': 'arn:aws:sqs:us-west-2:123456789012:my-queue',
        'Input': '{"queueKey": "queueValue"}'
    }
]

try:
    eventbridge_manager.update_targets(rule_name, new_targets)
    print(f"Successfully updated targets for rule: {rule_name}")
except Exception as e:
    print(f"Error updating targets: {str(e)}")
