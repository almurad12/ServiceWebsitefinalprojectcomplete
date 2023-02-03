from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login,logout
from .models import User
from account import views
# from cart.models import Cart
from cartanother.models import Cartanother
## call service model
from service.models import Sheba
from  cartanother.models import Cartanother
from  cartanother.models import Cartanothernew
from django.db.models import Count
from account.models import User
from django.db.models import Q
from cartanother.models import Order
from cartanother.models import Ordernew
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# from .urls import views


# def home(request):
#     return render(request,'buyinguserpage1.html')
def home(request):
    category = request.GET.get('category')
    minimum = request.GET.get('minimum')
    maximum = request.GET.get('maximum')
    print(category)
    print(minimum)
    print(maximum)
    context={}
    if minimum and maximum:
        context["servicedataset"]= Sheba.objects.filter(serviceprice__range=(minimum, maximum))
        context['feature']=Sheba.objects.filter(featureservice=True)
        context['minimumvalue']=minimum
        context['maximumvalue']=maximum

    elif category:
        context["servicedataset"] = Sheba.objects.filter(servicecategory=category)
        context['feature']=Sheba.objects.filter(featureservice=True)
    else:
        context["servicedataset"] = Sheba.objects.all()
        context['feature']=Sheba.objects.filter(featureservice=True)
    # return render(request,'slider.html',context)
    return render(request,'slider3.html',context)
    # return render(request,'Home.html',context)

###seller dashboard page
def sellerdashboard(request):
    return render(request,'4sellerdashboard.html')

###seller pending order page
def sellerpendingorder(request):
    context={}
    context['sellerpendingorder']=Ordernew.objects.filter(serviceuserid=request.user.id)
    return render(request,'service/sellerpendingorder.html',context)

@csrf_exempt
def buyerdashboard(request):
    context={}
    category =request.GET.get('category')
    minimum = request.GET.get('minimum')
    maximum = request.GET.get('maximum')

    if minimum and maximum:
        context["servicedataset"]= Sheba.objects.filter(serviceprice__range=(minimum, maximum))
        context['minimumvalue']=minimum
        context['maximumvalue']=maximum
        ###old
        carts = Cartanothernew.objects.filter(user_id = request.user.id)
        context['cartcount']= len(carts)
        context['cartvalue']=carts
        # context['addtocart']=Cartanother.objects.all()
        context['addtocart']=Cartanothernew.objects.all()
        ##for feature service
        context['feature']=Sheba.objects.filter(featureservice=True)

    elif category:
        context["servicedataset"] = Sheba.objects.filter(servicecategory=category)
        carts = Cartanothernew.objects.filter(user_id = request.user.id)
        context['cartcount']= len(carts)
        context['cartvalue']=carts
        # context['addtocart']=Cartanother.objects.all()
        context['addtocart']=Cartanothernew.objects.all()
        ##for feature service
        context['feature']=Sheba.objects.filter(featureservice=True)
        
    else:
        context["servicedataset"] = Sheba.objects.all()
        carts = Cartanothernew.objects.filter(user_id = request.user.id)
        context['cartcount']= len(carts)
        context['cartvalue']=carts
        # context['addtocart']=Cartanother.objects.all()
        context['addtocart']=Cartanothernew.objects.all()
        #for featureservice
        context['feature']=Sheba.objects.filter(featureservice=True)

    # data = Cart.objects.filter(user_id = request.user.id).select_related('service')
    # print(data[0].service)
    # return JsonResponse(list(data.values()),safe=False)
    # for cart in carts:
    #     context['cartcount'] += 1
    # print( context["cartcount"])
    # context["cartcount"]= Cart.objects.get()
    # return render(request,'7BuyerServicepage.html',context)

    # return render(request,'slider2.html',context)
    return render(request,'slider4.html',context)

# def login_view(request):
#     return render(request,'login.html')






# Create your views here.


# def index(request):
#     return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')

        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_buyer:
                login(request, user)
                return redirect('buyerdashboard')
            elif user is not None and user.is_seller:
                login(request, user)
                return redirect('sellerdashboard')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

###logout view
def logout_view(request):
    logout(request)
    return redirect('home')

def admin(request):
    return render(request,'admin.html')


def customer(request):
    return render(request,'customer.html')


def employee(request):
    return render(request,'employee.html')

def buyerorder(request):
    context={}
    context['createdorder'] = Ordernew.objects.filter(userid = request.user.id)
    return render(request,'buyerorderpage.html',context)

def cancelorder(request,id):
    # return render (request,'buyerorderpage.html')
    deleteorder = Ordernew.objects.filter(id = id)
    deleteorder.delete()
    # return redirect('/account/buyerorder/')
    # return redirect('/account/sellerpendingorder/')
    return redirect('/account/buyerorder/')
    

def editorder(request):
    id = request.GET.get('id')
    print(id)
    editorder = Ordernew.objects.filter(id = id)
    editorder.update(accept_or_rejected=True)
    # print(editorder['cartid'])
    # user=user_id,service=service_id
    # editorder =Ordernew(id=id,accept_or_rejected=1)
    # editorder.save()
    return redirect('/account/sellerpendingorder/')
