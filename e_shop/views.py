from django.shortcuts import render,redirect ,HttpResponse
from app.models import Category,Product,Contact_us,Order,Brand
from django.contrib.auth import  authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User


def master(request):
    return render(request,'master.html')


def index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all()
    brandid = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    elif(brandid):
        product = Product.objects.filter(brand=brandid).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        'product':product,
        'category':category,
        'brand':brand,
    }
    return render(request,'index.html' , context)

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password= form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    context={
        'form':form
    }
    return render(request,'sign_up.html',context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def contact_page(request):
    if request.method=='POST':
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request,'contact.html')


def Checkout(request):
    if request.method=="POST":
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)

        for i in cart:
            tot = (int(cart[i]['price']))*(int(cart[i]['quantity']))
            order = Order(
                user=user,
                product=cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone=phone,
                pincode=pincode,
                total = tot,
            )
            order.save()
        request.session['cart']={}
        return redirect('index')
    return HttpResponse("successfully checkout")

def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id =uid)
    order =  Order.objects.filter(user =user)
    context = {
        'order':order,
    }
    return render(request,'order.html',context)

def product_value(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all()
    brandid = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    elif(brandid):
        product = Product.objects.filter(brand=brandid).order_by('-id')
    else:
        product = Product.objects.all()


    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,'product.html',context)

def product_detail(request , id):
    product = Product.objects.filter(id=id).first()
    context = {
        'product':product,
    }

    return render(request,'product_detail.html',context)

def search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product':product,
    }
    return render(request,'search.html',context)