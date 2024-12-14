from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_registration_email(user, event):
    """
    Відправляє email підтвердження реєстрації на подію.
    """
    subject = f'Registration Confirmation - {event.title}'
    
    context = {
        'user': user,
        'event': event,
    }
    
    html_message = render_to_string('events/email/registration_confirmation.html', context)
    plain_message = render_to_string('events/email/registration_confirmation.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    ) 