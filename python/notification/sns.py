import boto3

class SNSNotificationSender:

    def __init__(self, enabled, region_name='sa-east-1') -> None:
        self.client = boto3.client('sns', region_name=region_name)
        self.enabled= enabled 

    def publish(self, arn_topic: str, subject: str, message: str) -> bool:
        """Publish a message for a given SNS topic."""

        if(self.enabled is False):
            return False

        if not arn_topic:
            raise ValueError('ARN Topic not configured')
        
        try:
            sns_response = self.client.publish(
                TopicArn=arn_topic,
                Message=message
                Subject=subject
            )

            if 'MessageId' in sns_response:
                return True

        except Exception as exception:
            pass
            
        return False

# USAGE EXAMPLE
            
sns_sender = SNSNotificationSender(enabled=True)

send_status = sns_sender.publish(
    arn_topic='arn:aws:sns:region:account-id:topic-name',
    subject='Important Alert', 
    message='This is a important alert sent through SNS.'
)

if send_status:
    print("The notification has been sent successfully.")
else:
    print("Failed publishing the message.")