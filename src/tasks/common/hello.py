from celery import shared_task


@shared_task
def hello(to):
    return 'Hello {0}'.format(to)
