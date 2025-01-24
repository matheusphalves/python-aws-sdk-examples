import boto3
from typing import Dict, Any, List
from botocore.exceptions import ClientError


class ECSManager:

    def __init__(self, region_name='sa-east-1') -> None:
        self.client = boto3.client('ecs', region_name=region_name)

    def get_tasks_by_service(self, cluster_name: str, service_name: str, desired_status: str):
        try:
            if desired_status:
                return self.client.list_tasks(
                    cluster=cluster_name,
                    serviceName=service_name,
                    desiredStatus=desired_status,
                    maxResults=100
                )

            desired_status = ['PENDING', 'RUNNING', 'STOPPED']
            results = {'taskArns': []}
            for desired_status in desired_status:

                results['taskArns'] += self.client.list_tasks(
                    cluster=cluster_name,
                    serviceName=service_name,
                    maxResults=100,
                    desiredStatus=desired_status
                ).get('taskArns', [])

            return results

        except ClientError as exception:
            raise Exception(f'Failed to get tasks of service {service_name}', original_exception=exception)

    def get_tasks(self, cluster_name: str, task_definition_family: str, desired_status: str):
        try:

            if desired_status:
                return self.client.list_tasks(
                    cluster=cluster_name,
                    family=task_definition_family,
                    desiredStatus=desired_status,
                    maxResults=100
                )

            desired_status = ['PENDING', 'RUNNING', 'STOPPED']
            results = {'taskArns': []}
            for desired_status in desired_status:

                results['taskArns'] += self.client.list_tasks(
                    cluster=cluster_name,
                    family=task_definition_family,
                    maxResults=100,
                    desiredStatus=desired_status
                ).get('taskArns', [])

            return results

        except ClientError as exception:
            raise Exception(f'Failed to get tasks of family {task_definition_family}',
                                 original_exception=exception)

    def describe_task(self, cluster_name: str, tasks: list, include=['TAGS']):
        try:

            return self.client.describe_tasks(
                cluster=cluster_name,
                tasks=tasks,
                include=include
            )

        except ClientError as exception:
            raise Exception(f'Failed to describe tasks {tasks}', original_exception=exception)


    def get_services(self, cluster_name: str, service_name: str) -> Dict[str, Any]:

        try:

            service_arns = [service_name]

            if service_name == '':
                # Search all the first 100 services given a cluster identififer
                service_arns = self.client.list_services(
                    cluster=cluster_name,
                    maxResults=100
                )['serviceArns']


            return self.client.describe_services(
                cluster=cluster_name, 
                services=service_arns
            )
            
        except ClientError as exception:
            raise Exception(f'Failed to get service description', original_exception=exception)

    def update_service(self, cluster_name: str, service_name: str, container_definition_name: str) -> str:

        try:

            return self.client.update_service(
                cluster=cluster_name,
                service=service_name,
                taskDefinition=container_definition_name,
                forceNewDeployment=True
            )
        
        except ClientError as exception:
            raise Exception(f'Problems updating service {service_name} with task definition {container_definition_name}: {str(exception)}')
    
    def restart_service(self, cluster_name: str, service_name: str) -> str:

        try:

            return self.client.update_service(
                cluster=cluster_name,
                service=service_name,
                forceNewDeployment=True,
                enableExecuteCommand=True,
            )
        
        except ClientError as exception:
            raise Exception(f'Problems restarting the service {service_name}: {str(exception)}')
        
    def execute_command(self, cluster_name: str, task_id: str, container_name: str, command: str) -> dict:
        
        try:
            return self.client.execute_command(
                cluster=cluster_name,
                task=task_id,
                container=container_name,
                command=command,
                interactive=True
            )
        except ClientError as exception:
            raise Exception(f'Failed to execute command in container {container_name}: {str(exception)}')


    def describe_task_definition(self, task_definition_name: str, include: List[str]=[]) -> Dict[str, Any]:
        
        try:
            if len(include) > 0:
                return self.client.describe_task_definition(
                    taskDefinition=task_definition_name,
                    include=include
                ) 
            
            return self.client.describe_task_definition(
                taskDefinition=task_definition_name
            )
            
        except ClientError as exception:
            raise Exception(f'Error describing task definition {task_definition_name}: {str(exception)}')
    

    def list_task_definitions(self, family_prefix: str) -> List[Dict[str, Any]]:
        
        task_definitions = []

        try:
            task_definitions = self.client.list_task_definitions(
                familyPrefix=family_prefix
            )

        except ClientError as exception:
            pass

        return task_definitions
    
    def clone_last_task_definition(self, 
            image: str,
            task_definition: Dict[str, Any], 
            remove_args: List[str], 
            include: List[str]=['TAGS']
        ) -> Dict[str, Any]:

        try:

            task_definitions = self.list_task_definitions(
                family_prefix=task_definition
            )

            if len(task_definitions.get('taskDefinitionArns', [])) == 0:
                raise Exception(f'Task definition not found for familyPrefix {task_definition}')

            task_definition = self.describe_task_definition(
                task_definition_name=task_definitions['taskDefinitionArns'][-1], 
                include=include
            )

            cloned_task_definition = task_definition['taskDefinition']
            task_definition_tags = task_definition['tags']
            cloned_task_definition['containerDefinitions'][0]['image'] = image

            for arg in remove_args:
                cloned_task_definition.pop(arg)


            return self.register_task_definition(
                task_definition=cloned_task_definition, 
                tags=task_definition_tags
            )

        except Exception as exception:
            raise Exception(f'Failed to clone the latest task definition of family {task_definition}: {str(exception)}')
    
    def register_task_definition(self, task_definition: Dict[str, Any], tags: Dict[str, Any]) -> str:
        
        try:

            if len(tags) > 0:
                return self.client.register_task_definition(**task_definition, tags=tags)
            
            return self.client.register_task_definition(**task_definition)

        except ClientError as exception:
            raise Exception(f'Failed to register task definition: {str(exception)}')
        
# USAGE EXAMPLE
ecs_manager = ECSManager(region_name='sa-east-1')

cluster_name = 'my-cluster'
service_name = 'my-service'

print(f"Getting details of service '{service_name}' in cluster '{cluster_name}'...")
service_details = ecs_manager.get_services(cluster_name, service_name)

print(f"Service details for '{service_name}':")
print(service_details)

new_task_definition = 'my-task-definition'
print(f"\nUpdating service '{service_name}' with new task definition '{new_task_definition}'...")
update_response = ecs_manager.update_service(cluster_name, service_name, new_task_definition)

print(f"Service update response:")
print(update_response)

print(f"\nRestarting service '{service_name}'...")
restart_response = ecs_manager.restart_service(cluster_name, service_name)

print(f"Service restart response:")
print(restart_response)
