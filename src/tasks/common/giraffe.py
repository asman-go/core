from celery import shared_task


@shared_task
def giraffe(to):
    return 'Giraffe {0}'.format(to)
