
import os
from celery import Celery
from django.core.mail import send_mail


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Social_Media.settings")
app = Celery("Social_Media")
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {'Send_mail_to_Client': {'task': 'Social_Media_app.tasks.send_mail_func','schedule': 30.0, }}
                          


app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


