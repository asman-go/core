import pydantic
from pubsub import pub, core

# listener = core.listener.UserListener()


class Domain(pydantic.BaseModel):
    domain: str


class Task(core.listener.UserListener):
    def __init__(self, topicName: str):
        self.topicName = topicName

    def subscribe(self):
        print('Task', 'subscribe', self.topicName)

    def __call__(self, message: Domain, **kwargs):
        print('Task', '__call__', self.topicName, message)


if __name__ == '__main__':
    TOPIC_NAME = 'domain'
    message = Domain(
        domain='example.com'
    )

    task = Task(TOPIC_NAME)

    pub.subscribe(task, task.topicName)
    pub.sendMessage(
        TOPIC_NAME,
        message=message,
    )
