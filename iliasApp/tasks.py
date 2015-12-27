from models import SampleCounting

from celery import task
# NOTE THAT THIS FILE IS FOR CELERY
@task()
def add_to_count():
    try:
        sc = SampleCounting.objects.get(pk=1)
    except:
        sc = SampleCounting()
    sc.num = sc.num + 1
    sc.save()


