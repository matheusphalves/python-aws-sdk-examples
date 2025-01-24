import boto3

class CloudWatchAlarmCreator:
    def __init__(self, region_name='sa-east-1'):
        self.region_name = region_name
        self.client = boto3.client('cloudwatch', region_name=region_name)

    def put_metric_alarm(self, alarm_dict):
        try:
            return self.client.put_metric_alarm(
                AlarmName=alarm_dict.get('AlarmName', ''),
                AlarmDescription=alarm_dict.get('AlarmDescription', ''),
                ActionsEnabled=alarm_dict.get('ActionsEnabled', False),
                OKActions=alarm_dict.get('OKActions', []),
                AlarmActions=alarm_dict.get('AlarmActions', []),
                InsufficientDataActions=alarm_dict.get('InsufficientDataActions', []),
                MetricName=alarm_dict.get('MetricName', ''),
                Namespace=alarm_dict.get('Namespace', ''),
                Statistic=alarm_dict.get('Statistic', ''),
                Dimensions=alarm_dict.get('Dimensions', []),
                Period=alarm_dict.get('Period', 1),
                EvaluationPeriods=alarm_dict.get('EvaluationPeriods', 1),
                DatapointsToAlarm=alarm_dict.get('DatapointsToAlarm', 1),
                Threshold=alarm_dict.get('Threshold', 100.0),
                ComparisonOperator=alarm_dict.get('ComparisonOperator', 'GreaterThanOrEqualToThreshold'),
                TreatMissingData=alarm_dict.get('TreatMissingData', ''),
                Tags=alarm_dict.get('Tags', [])
            )
        except Exception as ex:
            raise Exception(f"Failed to create metric_alarm {alarm_dict.get('AlarmName', '')}: {str(ex)}")

    def batch_put_metric_alarms(self, alarms: list):
        
        status = {}
        
        for alarm_data in alarms:
            try:
                response = self.put_metric_alarm(alarm_dict=alarm_data)
                status[alarm_data.get('AlarmName')] = {'status': True, 'response': response}
            except Exception as ex:
                status[alarm_data.get('AlarmName')] = {'status': False, 'error': str(ex)}
        
        return status
    

# USAGE EXAMPLE
cw_alarm_creator = CloudWatchAlarmCreator(region_name='sa-east-1')
service_01_alarms = [
            {
            "AlarmName": f"Alarm for ECS Service",
            "ActionsEnabled": True,
            "OKActions": [
                'arn:aws:sns:<REGION>:<ACCOUNT_ID>:<TOPIC_NAME>'
            ],
            "AlarmActions": [
                'arn:aws:sns:<REGION>:<ACCOUNT_ID>:<TOPIC_NAME>'
            ],
            "InsufficientDataActions": [],
            "MetricName": "RunningTaskCount",
            "Namespace": "ECS/ContainerInsights",
            "Statistic": "Average",
            "Dimensions": [
                {
                    "Name": "ServiceName",
                    "Value": "my-service"
                },
                {
                    "Name": "ClusterName",
                    "Value": "my-clsuter"
                }
            ],
            "Period": 300,
            "EvaluationPeriods": 3,
            "DatapointsToAlarm": 2,
            "Threshold": 1,
            "ComparisonOperator": "LessThanThreshold",
            "TreatMissingData": "missing"
        }
]
response_01 = cw_alarm_creator.batch_put_metric_alarms(alarms=service_01_alarms)