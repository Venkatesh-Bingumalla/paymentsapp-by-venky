from django.shortcuts import render
import razorpay
from .models import payments
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')
def home(request):
    flag=False
    if request.method=="POST":
        name=request.POST.get("name")
        email = request.POST.get("email")
        amount=request.POST.get("amount")
        if email!='' and name!='' and amount!='':
            amount=int(amount)
            if amount<0:
                flag=True
                messages.warning(request, 'Please Enter the Positive amount.')
                return render(request,'home.html',{'f':flag})
            else:
                amount*=100
            
                
                
                client=razorpay.Client(auth =("rzp_test_ZeRLUFQpel2sO4","vJEZJUII3XgH5vJgJjwIaMFF"))
                payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
                p=payments.objects.create(name=name ,email=email,amount=amount,payment_id=payment['id'])
                p.save()
                return render(request,'home.html',{'payment':payment})
        else:
            flag=True
            messages.warning(request, 'Please Enter all the details.')
            return render(request,'home.html',{'f':flag})
    else:
        return render(request,'home.html')   
def success(request):
    if request.method=="POST":
        a=request.POST
        order_id=""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id=val
                break
        user = payments.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
        msg_plain = render_to_string('email.txt')
        msg_html =render_to_string('email.html')
        send_mail("Your Donation"+" "+str(int(user.amount)//100)+" "+"has been received",msg_plain,settings.EMAIL_HOST_USER,[user.email],html_message=msg_html)
        
        return render(request,'success.html')