from django.shortcuts import render,redirect
from .models import Product, AddItem,Registration
from django.conf import settings
from project.settings import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

# Create your views here.
def Index(request):
    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
    return render(request,'index.html',{'leng':leng,'logindetails':logindetails,'adminDetails':adminDetails})
    
def About(request):
    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
    return render(request,'about.html',{'leng':leng,'logindetails':logindetails,'adminDetails':adminDetails})

def AddProduct(request):
    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
    return render(request,'Additem.html',{'leng':leng,'adminDetails':adminDetails})


def Productdata(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('img')

        AddItem.objects.create(Name = name,
                                 Price = price,
                                  Image = image)
        
        addtocart = request.session.get('addtocart')
        leng = 0
        if addtocart:
           leng=len(addtocart)
        return render(request,'AddItem.html',{'leng':leng})

def allProduct(request):
    item = AddItem.objects.all()
    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
   
    return render(request,'Products.html',{'item':item, 'media_url':settings.MEDIA_URL,'leng':leng,'logindetails':logindetails,'adminDetails':adminDetails})


def AddToCart(request,pk):
    if request.method == "POST":
        addtocart = request.session.get('addtocart',[])
        addtocart.append(pk)
        request.session['addtocart'] = addtocart   # for again put change value in session
        # return redirect('Product')
        item = AddItem.objects.all()
        leng = 0
        if addtocart:
           leng=len(addtocart)
        return render(request,'Products.html',{'item':item,'media_url':settings.MEDIA_URL,'leng':leng,'logindetails':logindetails})
    
def Cart(request):
    addtocart = request.session.get('addtocart')
    
    Cartdetails = []
    TotalAmount = 0
    leng = 0
    if addtocart:
       leng=len(addtocart)
    
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':MEDIA_URL,'TotalAmount':TotalAmount,'leng':leng,'logindetails':logindetails})


def Delete(request,pk):
    addtocart = request.session.get('addtocart')
    addtocart.remove(pk)
    request.session['addtocart'] = addtocart
    
    Cartdetails = []
    TotalAmount = 0
    leng = 0
    if addtocart:
       leng=len(addtocart)
    
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':MEDIA_URL,'TotalAmount':TotalAmount,'leng':leng,'logindetails':logindetails})


def Payment(request):
    global payment
    amount = int(request.POST.get('amount'))
    amunts=amount*100

    client = razorpay.Client(auth=("rzp_test_3LJ7CBlMbFfwT6","4thIATbNrfvi0N6mdFDThupO"))

    data = { "amount": amunts, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)

    Product.objects.create(amount=amount, order_id=payment['id'])

    addtocart = request.session.get('addtocart')
    Cartdetails = []
    TotalAmount = 0
    leng = 0
    if addtocart:
       leng=len(addtocart)
    for i in addtocart:
        data = AddItem.objects.get(id=i)
        context={
            'id':data.id,
            'Nm':data.Name,
            'Pr':data.Price,
            'Img':data.Image,
        }
        TotalAmount+=data.Price
        Cartdetails.append(context)
    return render(request,'Cart.html',{'Cartdetails':Cartdetails,'media_url':MEDIA_URL,'TotalAmount':TotalAmount,'payment':payment,'leng':leng,'logindetails':logindetails})


@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        response = request.POST

        razorpay_data = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth =("rzp_test_3LJ7CBlMbFfwT" , "4thIATbNrfvi0N6mdFDThupO"))

        try:
            status = client.utility.verify_payment_signature(razorpay_data)
            product = Product.objects.get(order_id=response['razorpay_order_id'])
            product.razorpay_payment_id = response ['razorpay_payment_id']
            product.paid = True
            product.save()

            addtocart = request.session.get('addtocart')
            for i in addtocart:
                data = AddItem.objects.get(id=i)
                # context={
                #     'id':data.id,
                #     'Nm':data.Name,
                #     'Pr':data.Price,
                #     'Img':data.Image,
                # }
            invoice_data = {
                "type": "invoice",
                "customer": {
                    "name": "customer name", # give name in name value
                    "contact":"9657758586",
                    "email":"indrajeetyadu36@gmail.com",
                    "billing_address" :"CybromTechnology MP Nagar Zone-1, Bhopal Madhya Pradesh", 
                    "shipping_address":"kolar road bhopal",  #change this address
                },
                "line_items": [data.id,data.Name,data.Price,data.Image], #ieme product ki list pass kar dena
            }
            invoice = client.invoice.create(data=invoice_data)
            
            return render(request, 'success.html', {'status': True})
        except:
            return render(request, 'success.html', {'status': False})


def Contact(request):
    # if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('msg')

    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
    
    #  For mail    
    subject='Test_mail for Query'
    message=message
    from_email=email
    recipient_list=['arpitkhare14@gmail.com','sumitumariya11@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    
    return render(request,'Contact.Html',{'leng':leng,'logindetails':logindetails})


def Registerdata(request):
    if request.method == "POST":
        name = request.POST.get('name') 
        email = request.POST.get('email') 
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        data = Registration.objects.filter(Email = email)

        if data:
            msg = "Already Exits"
            return render(request,'Register.html',{'msg':msg})
        else:
            if password == cpassword:
                Registration.objects.create(Name = name,
                                            Email = email,
                                            Password = password)
                msg= "Successfully Register"
                return render(request,'Login.html',{'msg':msg})
            else:
                msg = "Password Does not match"
                return render(request,'Register.html',{'msg':msg})

logindetails = {}
adminDetails = {}

def LoginData(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    role = request.POST.get('role')

    if role == "admin":
        if email == 'admin@gmail.com' and password == '1234':
            request.session['email'] = email
            request.session['password'] = password

            global adminDetails
            adminDetails={
                'AE':request.session.get('email'),
                'AP':request.session.get('password')
            }
            print('arpit',adminDetails)
            return render(request,'Index.html',{'adminDetails':adminDetails})
        else: 
            msg = "Invalid Email or password"
            return render(request,"Login.html",{'msg':msg})
    else:     
        user = Registration.objects.filter(Email = email)

        if user:
            data = Registration.objects.get(Email = email)
            passs = data.Password

            if passs == password:
                request.session['name'] = data.Name
                request.session['email'] = data.Email
                request.session['password'] = data.Password

                Nm=request.session.get('name')
                Em=request.session.get('email')
                Ps=request.session.get('password')

                global logindetails

                logindetails = {
                    'Nm':Nm,
                    'Em':Em,
                    'Ps':Ps
                }
                return render(request,'Index.html',{'logindetails':logindetails})
            else:
                msg = "Password does not match"
                return render(request,'Login.html',{'msg':msg})
        else:
            msg = "Enter valid Email"
            return render(request,'Login.html',{'msg':msg})
    
    
def Login(request):
    addtocart = request.session.get('addtocart')
    leng = 0
    if addtocart:
       leng=len(addtocart)
    return render(request,'Login.html',{'leng':leng})

def Register(request):
    return render(request,'Register.html')

def Logout(request):
    return render(request,'Login.html')

