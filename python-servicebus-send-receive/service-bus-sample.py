from azure.servicebus import ServiceBusService, Message, Queue

# Create ServiceBus client.
queue_client = ServiceBusService(
    # The name you assign to your servicebus instance during creation.
    service_namespace='<YOUR-SERVICEBUS-NAMESPACE>',
    # You can have multiple named keys, this parameter if the name of the key.
    # The value below is the name of the default key.
    # This can be found on the portal.
    shared_access_key_name='RootManageSharedAccessKey',
    # The key's value.
    # This can be found on the portal.
    shared_access_key_value='<YOUR-KEY>')

# The name we gave to our queue
queue_name = "<YOUR-SERVICEBUS-QUEUE-NAME>"

# You can create a queue from the portal or programmatically
def createQueue(queue_name):
    # Create Queue
    queue_options = Queue()

    # A queue can have a max size of 5GB.
    # i.e. the total size of messages we didn't consume cannot exceed 5GB.
    queue_options.max_size_in_megabytes = '5120'

    # Message time to live determines how long a message will stay in the queue before it expires and is removed or dead lettered.
    # Defaults to 14 days
    queue_options.default_message_time_to_live = 'PT1M'

    queue_client.create_queue(queue_name, queue_options)

def sendMessage(message):
    msg = Message(message)
    queue_client.send_queue_message(queue_name, msg)

def receiveMessage():
    # Receive message from queue. The message is removed from queue automatically.
    msg = queue_client.receive_queue_message(queue_name, peek_lock=False)
    print(msg.body)

def receiveMessageWithPeekLock():
    # Receive the message with peek lock enabled.
    msg = queue_client.receive_queue_message(queue_name, peek_lock=True)
    print(msg.body)

    # Remove the message from queue. If we didn't call this, the message would be released
    # back to the queue after the lock period. The lock period defaults to 30 seconds but
    # can be configured during queue creation to between 1 second and 5 minutes. 
    msg.delete()

receiveMessage()