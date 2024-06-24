from django.contrib.auth import get_user_model
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

@shared_task
def send_mail_func():
    users = list(get_user_model().objects.values_list('email', flat=True))
    # for user in users:
    mail_subject= "Hi! Testing of Celery"
    message= "Test Done SuccessFully Thankyou For Your Cooperation"
    email = EmailMessage(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        users
    )
    email.send()

# @app.task(Bind=True)
# def send_mail(first_name,email):
#     email= EmailMessage("Registration in Social Media App",f"Congrtulations {first_name}, You have successfully registered in the Application ",
#     settings.EMAIL_HOST_USER,[email])
#     email.send()