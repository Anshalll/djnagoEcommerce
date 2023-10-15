from django.shortcuts import render, redirect
from .models import ProductCat, Product, Users, Cart, Orders
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
def index(request):
    data = ProductCat.objects.all()
    params = {'data': data}
    return render(request, 'index.html', params)



def about(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'index.html')

def tracking(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'index.html')

def register(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        
        return redirect('/home')
    
    if request.method == "POST":
        username = request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        cpassword= request.POST['cpassword']
        firstname= request.POST['firstname']
        lastname= request.POST['lastname']
        phone= request.POST['phone']
        name = firstname + lastname
      
      
        form_data = {
                "username": username,
                "email": email,
                "pass": password,
                "cpass": cpassword,
                "fname": firstname,
                "lname": lastname,
                "phone": phone,
            }
      
       
        if not username or not email or not password or not cpassword or not firstname or not lastname or not phone:
            messages.error(request, "All fields are required" ,  extra_tags="error")
            return render(request , 'register.html', { "data" : form_data })
      
        fetch = Users.objects.filter(username = username)
        if fetch.exists():
            print("failed")
            messages.error(request, "Username is taken" ,  extra_tags="error")
            return render(request , 'register.html', { "data" : form_data })
        
        
        fetchEmail = Users.objects.filter(email = email)
        if fetchEmail.exists():
            messages.error(request, "Email address is Taken" , extra_tags="error")
            return render(request , 'register.html', { "data" : form_data })
                        
        if password != cpassword:
            messages.error(request, "Confirmed Password does not match!" , extra_tags="error")
            return render(request , 'register.html', { "data" : form_data })
        
        if not username.isalnum():
            messages.error(request, "Username can contain Numbers and Alphabets" , extra_tags="error")
            return render(request , 'register.html', { "data" : form_data })
        
        try: 
              validate_password(password)
              pass
        except Exception as e:

            messages.error(request, e.messages[0], extra_tags="error")
            return render(request, 'register.html', {"data": form_data})
           
         
        try: 
              validate_email(email)
              pass
        except Exception as e:

            messages.error(request, e.messages[0], extra_tags="error")
            return render(request, 'register.html', {"data": form_data})
        
        
        saveData = Users.objects.create(username = username, email=email, password=password, contact=phone, name=name)
        saveData.save()
        messages.success(request, "Data has been saved" , extra_tags="success")
        return redirect('/login')
       

        
    return render(request, 'register.html')

def login(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        
        return redirect('/home')
    
    if request.method == "POST":
        
        useremail = request.POST['useremail']
        password  = request.POST['password']
        
        form_data = {
                "useremail": useremail,
                "password": password,

             
            }
          
        if not useremail or not password:
            messages.error(request, "All fields are required" ,  extra_tags="error")
            return render(request , 'login.html', { "data" : form_data })
        
        
        fetch = Users.objects.filter(username= useremail) | Users.objects.filter(email= useremail)
        
        if fetch.exists():
            verifyPass = fetch.get()
            if password  == verifyPass.password:
                request.session['loggedin'] = True
                request.session['username'] = verifyPass.username
                request.session['email'] = verifyPass.email
                return redirect('/')
            else:
                messages.error(request, "Incorrect username or Password" ,  extra_tags="error")
                return render(request , 'login.html', { "data" : form_data })
        else:
            messages.error(request, "Incorrect username or Password" ,  extra_tags="error")
            return render(request , 'login.html', { "data" : form_data })   
            
            
    return render(request, 'login.html')

def categories(request):
        return render(request, 'index.html')


def productview(request, slug):
    data = Product.objects.filter(id = slug)
    params = {"data":data}
    return render(request, 'productview.html', params)


def products(request, slug):
    cat_instance = ProductCat.objects.get(poduct_cat_type=slug)
    products_in_category = Product.objects.filter(product_cat=cat_instance)
    
    params = {"data": products_in_category}
    
    return render(request, 'products.html', params)


def cart(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        fetcuser = Users.objects.filter(username = request.session.get("username"))
        fetchuserdata = fetcuser.get()
        fetchCart = Cart.objects.filter(Q(user_assoc=fetchuserdata.id) & Q(purchased=False))
        proudctData = []
        
        
        total_price = 0
        
        for i in fetchCart:
            
            pdata = Product.objects.filter(product_name = i.product_assoc)
            proudctData.append(pdata)
            data = pdata.get()
            cartqun = int(i.quantity)
            price = int(data.product_price)*cartqun
            total_price += price
        
        
        
        
        return render(request, "cart.html", {'productdata': proudctData, "cartdata": fetchCart, "totalprice": total_price})
    else:
        return redirect('/login')
    
    
    
    
def logout(request):
        request.session['loggedin'] = None
        request.session['username'] = None
        request.session['email'] = None
        
        
        return redirect('/')
    
def addtocart(request, slug):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        user  = request.session.get('username', 'default_value')
        try:
            
            #  ----------------------------
            # | fetch  the Product detail |
            # -----------------------------
            
            fetchProduct = Product.objects.filter(id =slug)
            getproduct = fetchProduct.get()
            
            #  ---------------------------
            # | fetch  the Users detail |
            # ----------------------------
                     
            fetchuser = Users.objects.filter(username = user)
            getUser = fetchuser.get()
            
            Cartexist = Cart.objects.filter(product_assoc = getproduct.id)
            
            if Cartexist.exists():
                messages.error(request, "Item Already Present in Cart" , extra_tags="error")
                return redirect(f'/productview/{slug}/')
            else:
                
                Cart.objects.create(user_assoc = getUser, product_assoc = getproduct )
                messages.success(request, "Product Added to Cart" , extra_tags="success")
                return redirect(f'/productview/{slug}/')
        
        
        except Exception as e:
            print(e)
            messages.error(request, 'An Error Occured' , extra_tags="error")
            return redirect(f'/productview/{slug}/')
    else:
        messages.error(request, 'Please Login into you account' , extra_tags="error")
        return redirect(f'/productview/{slug}/')
    
    
    
def cartupdateadd(request, slug):
    cart = Cart.objects.get(id=slug)  

    
    cart.quantity += 1
    
    
    cart.save()
    
 
    return redirect("/cart")


def cartdel(request , slug):
  cart = Cart.objects.get(id=slug)
  cart.delete()  
  return redirect("/cart")

def cartupdateremove(request , slug):
    
    cart = Cart.objects.get(id=slug)  

    if cart.quantity == 1:
        messages.error(request , "Quantity can not be less than 1, try deleting the product", extra_tags="error")
   
        
        return redirect("/cart")
    else:
        cart.quantity -= 1
        
        
        cart.save()
    
 
        return redirect("/cart")
    
def info(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        fetcuser = Users.objects.filter(username = request.session.get("username"))
        fetchuserdata = fetcuser.get()
        fetchCart = Cart.objects.filter(user_assoc = fetchuserdata.id)
        proudctData = []
        
        
        total_price = 0
        
        for i in fetchCart:
            
            pdata = Product.objects.filter(product_name = i.product_assoc)
            proudctData.append(pdata)
            data = pdata.get()
            cartqun = int(i.quantity)
            price = int(data.product_price)*cartqun
            total_price += price
        
            return render( request, "info.html", {"total_price": total_price})


            
    

def payment(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True and  request.method == "POST":
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        
        
        request.session['address'] = address
        request.session['city'] = city
        request.session['state'] = state
        request.session['zipcode'] = zipcode
        
        fetcuser = Users.objects.filter(username = request.session.get("username"))
        fetchuserdata = fetcuser.get()
        fetchCart = Cart.objects.filter(user_assoc = fetchuserdata.id)
        proudctData = []
        
        
        total_price = 0
        
        for i in fetchCart:
            
            pdata = Product.objects.filter(product_name = i.product_assoc)
            proudctData.append(pdata)
            data = pdata.get()
            cartqun = int(i.quantity)
            price = int(data.product_price)*cartqun
            total_price += price
            request.session['amount'] = total_price
  
        return render(request , "payment.html" , {"amount": request.session['amount']})
        


def orders(request):
    checkLogged = request.session.get('loggedin', 'default_value')
    if checkLogged == True:
        fetcuser = Users.objects.filter(username = request.session.get("username"))
        fetchuserdata = fetcuser.get()
        fetchCart = Cart.objects.filter(Q(user_assoc=fetchuserdata.id) & Q(purchased=True))
        proudctData = []
        
        
        total_price = 0
        
        for i in fetchCart:
            
            pdata = Product.objects.filter(product_name = i.product_assoc)
            proudctData.append(pdata)
            data = pdata.get()
            cartqun = int(i.quantity)
            price = int(data.product_price)*cartqun
            total_price += price
        
        
        
        
        return render(request, "orders.html", {'productdata': proudctData, "cartdata": fetchCart, "totalprice": total_price})
    else:
        return redirect('/login')
    
    
    
def userorders(request):
    if request.method == "POST":
        payment = request.POST['payment']
        checkLogged = request.session.get('loggedin', 'default_value')
    
        if payment == True and  checkLogged == True:
            fetcuser = Users.objects.filter(username = request.session.get("username"))
            fetchuserdata = fetcuser.get()
            fetchCart = Cart.objects.filter(Q(user_assoc=fetchuserdata.id) & Q(purchased=False))
            fetchCart.create(purchsed = False)
            Orders.objects.create(username = request.session.get("username"), state = request.session.get("state"), city = request.session.get("city"), zipcode = request.session.get("zipcode"), address = request.session.get("address"))
            Orders.save()
        return JsonResponse("Order Placed")
            
        
    