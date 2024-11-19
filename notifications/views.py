from django.shortcuts import render
from django.core.mail import send_mail
from .forms import SubscriptionForm
from .models import Subscriber
from django.conf import settings

def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            case_number = form.cleaned_data['case_number']

            # Save subscriber to the database
            Subscriber.objects.create(email=email, case_number=case_number)

            # Send confirmation email
            send_mail(
                'Confirmación de Suscripción',
                f'Usted a suscrito actualizaciones para el caso {case_number}. Legal Team le notificará por correo electrónico cuando haya actualizaciones.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return render(request, 'subscription_success.html', {'email': email, 'case_number': case_number})
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})
