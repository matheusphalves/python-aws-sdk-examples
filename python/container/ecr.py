import boto3
from botocore.exceptions import ClientError

class ECRManager:

    def __init__(self, region_name='sa-east-1') -> None:
        self.client = boto3.client('ecr', region_name=region_name)

    def list_images(self, repository_name: str, filter: dict = {'tagStatus': 'TAGGED'}) -> list:

        ecr_images = []
        try:

            ecr_images = self.client.describe_images(
                    repositoryName=repository_name, 
                    filter=filter
                )

        except ClientError as clientError:
            pass
        
        return ecr_images
    
    def find_image_by_tag(self, repository_name, tag: str, filter: dict = {'tagStatus': 'TAGGED'}):
        try:
            
            ecr_images = self.list_images(repository_name=repository_name, filter=filter)

            for ecr_image in ecr_images['imageDetails']:
                if tag in ecr_image['imageTags']:
                    return ecr_image

        except Exception as exception:
            raise Exception(f'Failed to get latest image within repository {repository_name} by tag {tag}: {str(exception)}')
            
# USAGE EXAMPLE
ecr_manager = ECRManager(region_name='sa-east-1')

repository_name = 'my-repository'
images = ecr_manager.list_images(repository_name)

if images.get('imageDetails'):
    print(f"Images found in '{repository_name}':")
    for image in images['imageDetails']:
        print(image['imageTags'])
else:
    print(f"No images found in repository '{repository_name}'.")


tag_to_search = 'v1.0.0'
image_by_tag = ecr_manager.find_image_by_tag(repository_name, tag=tag_to_search)

if image_by_tag:
    print(f"Image found with tag '{tag_to_search}':")
    print(image_by_tag)
else:
    print(f"No image found with tag '{tag_to_search}'.")
