import json
import websockets
import uuid
import datetime


class ECSExecuteCommandOutputCatcher:

    async def process_ecs_command_output(self, session_url: str, token_value: str) -> str:
        """
            # See the problem workaround for this problem here:
            # https://github.com/boto/boto3/issues/3496
            # https://github.com/theherk/interloper/issues/1
        """
        total_payload_message = ''
        already_seen = set()

        try:
            async with websockets.connect(session_url) as connection:

                print(f'Starting connection with WebSocket: {session_url}')

                init_payload = {
                    "MessageSchemaVersion": "1.0",
                    "RequestId": str(uuid.uuid4()),
                    "TokenValue": token_value
                }

                await connection.send(json.dumps(init_payload))

                while True:

                    response = await connection.recv()

                    deserialized_message = self.deserialize_message(response)

                    if not deserialized_message:
                        break

                    # Stream starts with this message, does not have to be ack
                    if deserialized_message['message_type'] == 'start_publication':
                        continue

                    # Break if this message is received
                    if deserialized_message['message_type'] == 'channel_closed':
                        break

                    # Process payload if it's output of our command
                    if deserialized_message['payload_type'] == 1:
                        payload_message = deserialized_message['payload']
                        if payload_message not in already_seen:
                            already_seen.add(payload_message)
                            total_payload_message += payload_message

                    connection.send(self.create_ack_message(deserialized_message))

        except Exception as e:
            print(f"Failed to catch output through WebSocket: {e}")
        finally:
            print('Closing connection...')
            await connection.close()

        return total_payload_message

    def create_ack_message(self, deserialized_message):

        ack_message_type = "acknowledge"
        ack_buffer = (len(ack_message_type)).to_bytes(4, "big")
        ack_buffer += ack_message_type.encode('utf-8').ljust(32, b'\x00')
        ack_buffer += (1).to_bytes(4, "big")
        ack_buffer += int(datetime.datetime.now().timestamp()).to_bytes(8, "big")
        ack_buffer += deserialized_message['sequence_num'].to_bytes(8, "big")
        ack_buffer += (1).to_bytes(8, "big")
        ack_buffer += uuid.uuid4().bytes
        ack_buffer += (2).to_bytes(4, "big")
        ack_buffer += (0).to_bytes(4, "big")
        ack_buffer += b''

        return ack_buffer

    def deserialize_message(self, response):
        """
        # Refer to the link below for structure and validation
        # https://github.com/aws/amazon-ssm-agent/blob/mainline/agent/session/contracts/agentmessage.go
        """
        response_length = len(response)

        if response_length == 0:
            return None
        elif response_length < 120:
            raise Exception('Cannot deserialize message')

        return {
            "message_type": response[4:36].decode("utf-8").strip('\x00'),
            "sequence_num": int.from_bytes(response[48:56], byteorder="big"),
            "payload_type": int.from_bytes(response[112:116], byteorder="big"),
            "payload": response[120:].decode('utf-8')
        }
    
# USAGE EXAMPLE
import asyncio

# Session URL and token value, which you would typically get from the ECS service
session_url = 'wss://example-ecs-session-url.com/socket'
token_value = 'example-token-value'

# Instantiate the ECSExecuteCommandOutputCatcher class
catcher = ECSExecuteCommandOutputCatcher()

# Asynchronously process ECS command output through the WebSocket connection
async def process_output():
    total_output = await catcher.process_ecs_command_output(session_url, token_value)
    
    # Print the captured output
    print(f"Captured ECS Command Output: {total_output}")

# Run the async function using asyncio event loop
asyncio.run(process_output())
