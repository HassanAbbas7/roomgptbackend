# views.py
import json
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from datetime import datetime, timedelta
from .stripeManager import *




stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors, status=400)
        


class Test(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        return Response("working")
    
    def get(self, request):
        user = CustomUser.objects.get(email="ph0150165@gmail.com")
        user.credits = 0
        user.save()
        return Response(user.credits)


class GetCredits(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        return Response(user.credits)
    

class GetCurrentPriceId(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        try:
            print(user.subscription.priceId)
        except Exception as e:
            print(e)
        return Response(user.subscription.priceId if user.subscription else False)




    
@permission_classes((AllowAny,))
@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, currency='pln', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

@permission_classes((AllowAny,))
@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data['amount']  # Amount in cents
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd'
            )
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def save_stripe_info(request):

  data = request.data
  email = data['email']
  payment_method_id = data['payment_method_id']
  extra_msg = '' # add new variable to response message



  customer_data = stripe.Customer.list(email=email).data
  
  


  # if the array is empty it means the email has not been used yet  
  if len(customer_data) == 0:
    # creating customer
    customer = stripe.Customer.create(
      email=email,
      payment_method=payment_method_id,
      invoice_settings={
        'default_payment_method': payment_method_id
      }
    )

  else:
    customerId = customer_data[0]["id"]
    subs = stripe.Subscription.list(customer=customerId)
    if len(subs) > 0:
      subId = subs.data[0].id
      subItemId = subs.data[0]["items"]["data"][0]["id"]
      subPriceId = subs.data[0]["items"]["data"][0]["price"]["id"]
    customer = customer_data[0]
    extra_msg = "Customer already existed."

  userIsSubscribed = request.user.subscription != None
  userPriceId = request.user.subscription.priceId

  if userIsSubscribed and userPriceId == data["priceId"] :
      print(request.data["priceId"])
      return Response(status=status.HTTP_200_OK, 
        data={'message': 'Failed', 'data': {
           'payment': 'failed', 'details':'Already Subscribed to this Subscription'}
      }) 
  

  elif len(subs) > 0:
      changeSubscription(subId=subId, subItemId=subItemId, newPriceId=data["priceId"], user=request.user)
      issueCredits(user=request.user, credits=data["credits"])
      return Response(status=status.HTTP_200_OK, 
        data={'message': 'Success', 'data': {
           'payment': 'success', 'details':'subscription changed'}
      }) 
  

  payment = stripe.Subscription.create(
    customer=customer,
    items=[
      {
       'price': data["priceId"] #here paste your price id
      }
    ]
  )
  assignSubscriptionToUser("any", stripeId=payment.id, user=request.user, priceId=data["priceId"])



  if payment.status == "active":
      issueCredits(request.user, data["credits"])

      return Response(status=status.HTTP_200_OK, 
        data={'message': 'Success', 'data': {
          'customer_id': customer.id, 'payment': payment.status}
      })  