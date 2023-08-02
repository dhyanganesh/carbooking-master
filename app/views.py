from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Contact, Product, Customer, Cart,OrderPlaced
from django.views import View
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, "home.html")


def userlogin(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("password")
        myuser = authenticate(username=uname, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentails")
            return redirect('login')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        confirmpassword = request.POST.get("pass2")

        if password != confirmpassword:
            messages.warning(request, "Password is Incorrect")
            return redirect('/register')

        try:
            if User.objects.get(username=uname):
                messages.info(request, "UserName Is Taken")
                return redirect('/register')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request, "Email Is Taken")
                return redirect('/register')
        except:
            pass

        myuser = User.objects.create_user(uname, email, password)
        myuser.save()
        messages.success(request, "Signup Successfull")
        return redirect('login')

    return render(request, 'register.html')


def userlogout(request):
    logout(request)
    messages.info(request, "logout successfull")
    return redirect('login')


@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        fname = request.POST.get("name")
        femail = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        query = Contact(name=fname, email=femail,
                        phoneNumber=phone, description=desc)
        query.save()
        messages.info(
            request, "Thanks For Reaching Us! We will get back you soon....")
        return redirect('contact')
    return render(request, 'contact.html')


class category(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        return render(request, "category.html", locals())


class productdetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "productdetails.html", locals())


def profile(request):
    if request.method == "POST":
        user = request.user
        fname = request.POST.get("fname")
        name = request.POST.get("name")
        lname = request.POST.get("lname")
        location = request.POST.get("location")
        email = request.POST.get("email")
        phone = request.POST.get("phoneno")
        state = request.POST.get("state")

        query = Customer(user=user, name=name, fname=fname, lname=lname,
                         location=location, email=email, phoneno=phone, state=state)
        query.save()
        messages.info(request, "saved sucessfully")
        return redirect("address")

    return render(request, "profile.html")


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "address.html", locals())


def updateaddress(request, pk):
    add = Customer.objects.get(pk=pk)
    if request.method == "POST":
        user = request.user
        add.fname = request.POST.get("fname")
        add.name = request.POST.get("name")
        add.lname = request.POST.get("lname")
        add.location = request.POST.get("location")
        add.email = request.POST.get("email")
        add.phone = request.POST.get("phoneno")
        add.state = request.POST.get("state")
        add.save()
        messages.info(request, "data saved")
        return redirect("address")

    return render(request, "updateaddress.html", locals())


def deleteaddress(request, pk):
    Customer.objects.filter(id=pk).delete()
    messages.info(request, "deleted successfully")
    return redirect("address")


def passwordchange(request):
    user = request.user
    print(user.password)
    if request.method == " POST":

        oldpass = request.POST.get("oldpass")

        newpass = request.POST.get("newpass")

        repeatpass = request.POST.get("repeatpass")

        if check_password(oldpass, user.password):
            print(True)
            messages.error(request, "old password is incorrect")

        elif newpass != repeatpass:
            messages.error(request, "new password not matching")

        else:
            user.password = make_password('newpass')
            print(user.password)
            messages.info(request, "your password is changed")
            user.save()
            return redirect(passwordchange)

    return render(request, "passwordchange.html", locals())


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    add = Customer.objects.filter(user=user)
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.selling_prize
        amount = amount+value
    totalamount = amount+500
    return render(request, 'addtocart.html', locals())


def deletecartitem(request, pk):
    Cart.objects.filter(id=pk).delete()
    messages.info(request, "deleted successfully")
    return redirect("showcart")


class checkout(View):
    def get(self, request):
        
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
       
        amount = 0
        for p in cart_items:
            value = p.quantity*p.product.selling_prize
            amount = amount+value
        totalamount = amount+500

        return render(request, "checkout.html", locals())

    def post(self, request):
        user=request.user
        custid=request.POST.get("custid")
        cart_items = Cart.objects.filter(user=user)
        cust=Customer.objects.get(id=custid)
        Cart(cust=cust).save
        for c in cart_items:
            OrderPlaced(user=user,customer=cust,product=c.product,quantity=c.quantity).save()
          
        return redirect("orders")


def orders(request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        ord=OrderPlaced.objects.filter(user=user)
        
        amount = 0
        for p in cart:
            value = p.quantity*p.product.selling_prize
            amount = amount+value
        totalamount = amount+5000

        messages.info(request, "your order has been placed")
        return render(request, "orders.html", locals())

def invoice(request,pk):
    user=request.user
    # orderdetails=OrderPlaced.objects.get(user=user)
    order=OrderPlaced.objects.filter(pk=pk)
    amount = 0
    for p in order:
        value = p.quantity*p.product.selling_prize
        amount = amount+value
    totalamount = amount+500

    return render(request,"invoice.html",locals())
