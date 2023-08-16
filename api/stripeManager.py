from .models import * 
from datetime import datetime, timedelta
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


def assignSubscriptionToUser(subscriptionName, stripeId, priceId, user):
    subscription = Subscription.objects.create(
        name=subscriptionName,
        stripeId=stripeId,
        priceId=priceId,
        nextInvoice=datetime.now().date() + timedelta(days=30)  # Adjust as needed
    )

    user = CustomUser.objects.get(email=user)
    user.subscription = subscription
    user.save()


def changeSubscription(subId, subItemId, newPriceId, user):
    payment = stripe.Subscription.modify(
      subId,
      items=[{"id": subItemId, "deleted": True}, {"price": newPriceId}],
    )
    user_ = CustomUser.objects.get(email=user)
    user_.subscription.priceId = str(newPriceId)
    user_.subscription.stripeId = str(payment.id)
    user_.nextInvoice=datetime.now().date() + timedelta(days=30)
    user_.subscription.save()

def issueCredits(user, credits):
    user_ = CustomUser.objects.get(email=user)
    user_.credits += int(credits)
    user_.save()