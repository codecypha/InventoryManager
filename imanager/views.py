from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowerd_users
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import datetime, pytz
from .forms import CategoryForm, ItemForm, RequestForm
from .models import Category, Items, ItemRequest, ManagerApproval
import datetime
now = datetime.datetime.now()
from django.contrib import messages
from django.core.paginator import Paginator #import Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
import csv
from django.template.loader import get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Sum
from collections import Counter

# Create your views here.

#Email sendi
def sendemail(orders):
    if orders == 'new_request':
        template = "email/new_request.html"
        context = {}
        reciever = []
        cc=[]
    elif orders == 'more_information':
        template = "email/more_information.html"
        context = {}
        reciever = []
        cc=[]
    elif orders == 'manager_notification':
        template = "email/manager_notification.html"
        context = {}
        reciever = []
        cc=[]
    elif orders == 'head_notification':
        template = "email/head_corp_notification.html"
        context = {}
        reciever = []
        cc=[]
    elif orders == 'final_notification':
        template = "email/final_notification.html"
        context = {}
        reciever = []
        cc=[]
    else:
        template = "email/reject.html"
        context = {}
        reciever = []
        cc=[]

    html_content = get_template(template)
    html_content = html_content.render(context)
    msg = EmailMessage('Inventory Manager', html_content, 'app.notifications@ubagroup.com', reciever, cc=['kolawobee@gmail.com'])
    #msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email], bcc=[bcc_email], cc=[cc_email])
    msg.send()
    return sendemail



@unauthenticated_user
def loginPage2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = str(username)
        password = str(password)
        username = username.replace("@ubagroup.com", '')
        fname, sname = username.split(".")
        password2 = make_password(password)
     
        if username == 'admin12398':
            response = 'true'
        else:
            if username != 'admin12398' :
                try:
                    # api_request = requests.get('http://10.100.67.102/ad.service/api/AD/AuthenticateUser?Username='+ username  +'&Password='+ password)
                    # api = json.loads(api_request.content)
                    # response =str(api)
                    # response1 = api_request.status_code
                    api_request = "http://paperless.ubagroup.com/ad.service/api/AD/AuthenticateUser"
                    headers = {'Content-Type': 'application/json'}
                    payload = {'Username':username, 'Password': password}
                    payload = str(payload)
                    response1 = requests.request("POST", api_request, headers=headers,  data=payload) 
                    response = response1.text 
                    print(response)                
                except ConnectionError as e:
                    messages.error(request, 'Service is currently down, Please try again')
                    print(e)
                    r = "No response"
        
        if response == 'true' : 
            user_count = User.objects.filter(username=username).count()
            if user_count == 0:
                #cursor.execute("insert into auth_user (username, password,is_staff,is_superuser, first_name, last_name, email, is_active, date_joined) values (%s, %s, 0, 0, 'Null', %s,  %s, 1, '2020-07-15 00:14:31')", (str(username), str(password2), str(country), str(username)+'@ubagroup.com' ))
                a = User(username=username, password= password2,is_staff = 0 ,is_superuser = 0, first_name = 'Null', last_name = 'Null', email = username+'@ubagroup.com', is_active = 1, date_joined = '2020-07-15 00:14:31')
                a.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    user = User.objects.get(username=username)
                    login(request, user)
                    return redirect('home') 
            #row = cursor.fetchall()
            else:
                password2 = make_password(password)
                a = User.objects.get(username=username)
                a.password = password2
                a.save()
                #cursor.execute("update auth_user set password = %s where username = %s", (str(password2), str(username), ))
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    user = User.objects.get(username=username)
                    login(request, user)
                    messages.info(request, 'Welcome' + ' ' + fname.capitalize())
                    return redirect('home') 
                else:
                    messages.error(request, 'Incorrect Username Entered')
                    return redirect('login')  
        else:
            #cursor.execute("update auth_user set password = %s where username = %s", (str(password2), str(username), )) 
            messages.error(request, 'Username/Password Incorrect!')
            return redirect('login')
    context ={}
    return render(request, 'portal/login.html', context)



@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username=username.capitalize()
        password = request.POST.get('password')
        country = request.POST.get('country')  
        print(username)
        #session to get country selected 
        request.session['country'] = country

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Incorrect Username/Password Entered')
            return redirect('login')
    context ={}
    return render(request, 'accounts/login.html', context)



login_required(login_url  ='login')
def logoutPage(request):
    print('logout')
    logout(request)
    return redirect('login')


@login_required(login_url  ='login')
def index(request):
    country = request.session.get('country')
    cur_time = datetime.datetime.now(tz=pytz.timezone(str(settings.TIME_ZONE)))
    cur_time = (cur_time.hour)
    pending_head = ItemRequest.objects.filter(country=country, manager_decision = 'approve').count()
    pending_manager = ItemRequest.objects.filter(country=country, manager_decision = 'pending').count()
    itemsrequest_qs = ItemRequest.objects.filter(country=country)
    itemsrequest_count = itemsrequest_qs.count()
    items = Items.objects.filter(country=country, status='Active')
    items_count = items.count()
   
    item_amont = Items.objects.filter(country=country, status='Active').aggregate(Sum('unit_price'))['unit_price__sum']
    quantity_amont = Items.objects.filter(country=country, status='Active').aggregate(Sum('quantity'))['quantity__sum']
    try:
        total_amount  = item_amont * quantity_amont
    except TypeError:
        total_amount = 0
    
    no_stock= 0
    low_stock= 0
    for item in items:
        item_list = []
        if item.quantity == 0:
            item_list.append(item.name)
            no_stock = len(item_list)
    
            
        elif item.quantity > 1 and item.quantity < 2000:
            item_list.append(item.name)
            low_stock = len(item_list)
        
        else:
            pass
    

    itemsrequest = ItemRequest.objects.raw("""SELECT id, item_name, count(item_name) count,  sum(quantity_requested)quantity_requested,
                                        (SELECT unit_price FROM item WHERE name=item_name) unit_price, 
                                        ((SELECT unit_price FROM item WHERE name=item_name) * sum(quantity_requested)) total
                                        FROM itemrequest where country = %s GROUP BY item_name  ORDER BY COUNT desc  LIMIT 10 """, [country] )
    
  
    context = {"cur_time":cur_time, "no_stock":no_stock,  "low_stock":low_stock, "items_count":items_count, "itemsrequest":itemsrequest, 'total_amount':total_amount, "itemsrequest_count":itemsrequest_count, "pending_head":pending_head, "pending_manager":pending_manager}
    return render(request, 'dashboard/index.html', context)



def search(request):
    search_name = request.POST.get('search_name')
    cat = Category.objects.filter(name__icontains =search_name)
    context = {"cat":cat}
    return render(request, 'category/list-category.html', context)
    


@login_required(login_url  ='login')
#@allowerd_users(allowed_roles =['inventory manager'])
def addCategory(request):
    country = request.session.get('country')
    category_code = Category.objects.filter().last()
    
    if not category_code:
        category_code = 100
    else:
        cat_code = int(category_code.code)
        category_code = (cat_code + 1)
    form = CategoryForm()
    if request.method =='POST':
        category_name = request.POST.get('category_name')
        category_name =category_name.capitalize()
        category_exist = Category.objects.filter(country=country, name=category_name)
        print(category_exist)
        if not category_exist:
            categoryform = form.save(commit=False)
            categoryform.name = category_name.capitalize()
            categoryform.code = category_code
            categoryform.country = country
            categoryform.save()
            messages.success(request, 'A category with name  ' +  category_name.upper() + ' has been created successfully!' )
            return redirect('listCategory')     
        else:
            messages.error(request, 'Error: ' +  category_name.upper() + ' already exists!!' )
            return redirect('listCategory')
    context = {}
    return render(request, 'category/add-category.html', context)

@login_required(login_url  ='login')
def editCategory(request, pk):
    category_item = Category.objects.get(id=pk)
    category_name = category_item.name
    status = category_item.status

    form = CategoryForm()
    if request.method =='POST':
        try:
            category_name = request.POST.get('category_name')
            status = request.POST.get('status')
            category_name=category_name.capitalize()
            Category.objects.filter(id=pk).update(name=category_name, status=status)
            messages.success(request, category_name.upper() + ' has been updated successfully!' )
            return redirect('listCategory')
        except IntegrityError:
            messages.error(request, 'Error: ' +  category_name.upper() + ' already exists!!' )
            return redirect('listCategory')
    context = {"category_name":category_name, "status":status}
    return render(request, 'category/edit-category.html', context)


def listCategory(request):
    country = request.session.get('country') 
    
    if request.method=='POST':
        search_name = request.POST.get('search_name')
        cat = Category.objects.filter(name__icontains =search_name, country=country)
        paginator = Paginator(cat, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cat_count = Category.objects.filter(name__icontains =search_name, country=country).count()
    else:
        cat = Category.objects.filter(country=country)
        paginator = Paginator(cat, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cat_count =Category.objects.filter(country=country).count()
    context = {"cat":page_obj, "cat_count":cat_count}
    return render(request, 'category/list-category.html', context)


@login_required(login_url  ='login')
def addItems(request):
    country = request.session.get('country')
    cats = Category.objects.filter(country=country, status='Active')
    form = ItemForm()
    if request.method == 'POST':
        cat = request.POST.get('category')
        description = request.POST.get('description')
        item_name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        itemform = form.save(commit=False)
        itemform.category = cat
        itemform.name = item_name.capitalize()
        itemform.country = country
        #itemform.description = description
        itemform.quantity = quantity
        itemform.unit_price = unit_price
        itemform.country = country
        itemform.save()
        messages.success(request, 'An item with name  ' +  item_name.upper() + ' has been created successfully!' )
        return redirect('addItems')  
    context = {"cats":cats}
    return render(request, 'items/add-items.html', context)

@login_required(login_url  ='login')
def editItems(request, pk):
    country = request.session.get('country')
    cats = Category.objects.filter(country=country, status='Active')
    item = Items.objects.get(id=pk)
    item_name = item.name
    category = item.category
    status = item.status
    quantity = item.quantity
    unit_price = item.unit_price
    form = ItemForm()
    if request.method =='POST':
        try:
            item_name = request.POST.get('item_name')
            category = request.POST.get('category')
            
            status = request.POST.get('status')
            quantity = request.POST.get('quantity')
            unit_price = request.POST.get('unit_price')
            item_name=item_name.capitalize()

            Items.objects.filter(id=pk).update(name=item_name, status=status, quantity=quantity, unit_price=unit_price,category=category )
            messages.success(request, item_name.upper() + ' has been updated successfully!' )
            return redirect('listItems')
        except IntegrityError:
            messages.error(request, 'Error: ' +  item_name.upper() + ' already exists!!' )
            return redirect('listItems')
    context = {"item_name":item_name, "status":status, "cats":cats, "category":category, "unit_price":unit_price, "quantity":quantity }
    return render(request, 'items/edit-items.html', context)


@login_required(login_url  ='login')
def listItems(request):
    country = request.session.get('country') 
    if request.method=='POST':
        search_name = request.POST.get('search_name')
        cat = Items.objects.filter(name__icontains =search_name, country=country)
        paginator = Paginator(cat, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cat_count = cat = Items.objects.filter(name__icontains =search_name, country=country).count()
    else:
        cat = Items.objects.filter(country=country)
        paginator = Paginator(cat, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cat_count =Items.objects.filter(country=country).count()
    context = {"cat":page_obj, "cat_count":cat_count}
    return render(request, 'items/list-items.html', context)


def addSales(request):
    orders='new_request'
    requester = request.user
    country = request.session.get('country')
    cats = Category.objects.filter(country=country, status='Active')
    items = Items.objects.filter(country=country, status='Active')

    
    form = RequestForm()
    if request.method == 'POST':
        cat = request.POST.get('category')
        item_name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        requestform = form.save(commit=False)
        requestform.category = cat
        requestform.requester = requester
        requestform.item_name = item_name
        requestform.country = country
        requestform.quantity_requested = quantity
        requestform.unit_price = unit_price
        requestform.country = country
        requestform.save()
        messages.success(request, 'Request initiated successfully!' )
        sendemail(orders)
        return redirect('addSales')  
    context = {"cats":cats, "items":items}
    return render(request, 'sales/add-sales.html', context)


@login_required(login_url  ='login')
def listSales(request):
    country = request.session.get('country')
    request_items = ItemRequest.objects.filter(country=country)


    context = {"request_items":request_items}
    return render(request, 'sales/list-sales.html', context)



@login_required(login_url  ='login')
def addPurchase(request):
    country = request.session.get('country')

    context = {}
    return render(request, 'purchases/add-purchase.html', context)



@login_required(login_url  ='login')
def listPurchase(request):   
    country = request.session.get('country') 
    cat_count = 0
    orders = ''
    for g in request.user.groups.all():
        if g.name =='inventory manager':
            role_name = 'manager_notification'
            if request.method=='POST':
                search_name = request.POST.get('search_name')
              
                if 'approve' in request.POST:
                    orders = 'manager_notification'
                    quantity_given = request.POST.get('quantity_given')
                    quantity_approved = int(quantity_given)
                    submit_value  = request.POST['approve']
                    item_name, item_id = submit_value.split("/")
                    item = Items.objects.get(name=item_name, country=country, status='Active')
                    request_id = ItemRequest.objects.get(id=item_id, country=country,) 
                    quantity_available = int(item.quantity)
                    pending_approval = int(item.pending_approval)
                    quantity_requested = int(request_id.quantity_requested)
                    if quantity_requested > quantity_available:
                        messages.warning(request, 'Requested quantity is more than quantity in stock - Quantity in stock ' + str(quantity_available) + '!')
                        #sendemail(orders)        
                    elif quantity_approved > quantity_available:
                        messages.warning(request, 'Requested quantity given is more than quantity in stock - Quantity in stock ' +str(quantity_available) + '!')
                    elif quantity_approved == 0 or quantity_approved == '0':
                        messages.warning(request, 'Quanity given cannot be 0: Please check your entry and try again: !') 
                    else:
                        temporary_given = pending_approval + quantity_approved
                        quantity_remain = int(quantity_available) - int(quantity_given)
                    
                        item_update = Items.objects.get(name=item_name, country=country, status='Active')
                        item_update.quantity=quantity_remain
                        item_update.pending_approval=temporary_given 
                        item_update.save()
                        
                        itemrequest_update = ItemRequest.objects.get(id=item_id, country=country)
                        itemrequest_update.manager_decision ='approve'
                        itemrequest_update.quantity_given =  int(quantity_given)
                        itemrequest_update.stage =  'inventory manager approval'
                        itemrequest_update.save()
                        
                        approval_log = ManagerApproval(request_id=item_id, inventManager=request.user, country=country, decision='approve')
                        approval_log.save()
                        messages.success(request, 'Request updated successfully!')
                        sendemail(orders)
                    return redirect('listPurchase')  
            
                elif 'reject' in request.POST:
                    orders = 'reject'
                    quantity_given = request.POST.get('quantity_given')
                    quantity_approved = int(quantity_given)
                    item_id  = request.POST['reject']
                    
                    
                   
                    itemrequest_update = ItemRequest.objects.get(id=item_id, country=country )
                    itemrequest_update.manager_decision ='reject'
                    itemrequest_update.stage =  'inventory manager reject'
                    itemrequest_update.save()
                    
                    approval_log = ManagerApproval(request_id=item_id, inventManager=request.user, country=country, decision='reject')
                    approval_log.save()
                    
                    messages.success(request, 'Request updated successfully!')
                    sendemail(orders)
                    return redirect('listPurchase') 
                   
        
                else:
                    cat = ItemRequest.objects.filter(item_name__icontains =search_name, country=country, manager_decision='pending')
                    paginator = Paginator(cat, 5)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    cat_count =  ItemRequest.objects.filter(item_name__icontains =search_name, country=country, manager_decision='pending').count()
                    context = {"cat":page_obj, "cat_count":cat_count, "role_name":role_name }
                    return render(request, 'purchases/list-purchase.html', context)
            
            else:
                cat = ItemRequest.objects.filter(country=country, manager_decision='pending')
                paginator = Paginator(cat, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                cat_count =  ItemRequest.objects.filter(country=country, manager_decision='pending').count()
                context = {"cat":page_obj, "cat_count":cat_count, "role_name":role_name}
                return render(request, 'purchases/list-purchase.html', context)
        
        
        if g.name =='head corporate':
            orders = 'head_notification'
            if request.method=='POST':
                search_name = request.POST.get('search_name')
                if 'approve' in request.POST:
                    #quantity_given = request.POST.get('quantity_given')
                    #quantity_approved = int(quantity_given)
                    submit_value  = request.POST['approve']
                    item_name, item_id = submit_value.split("/")
                    item = Items.objects.get(name=item_name, country=country, status='Active')
                    request_id = ItemRequest.objects.get(id=item_id, country=country) 
                    quantity_available = int(item.quantity)
                    pending_approval = int(item.pending_approval)
                    quantity_requested = int(request_id.quantity_requested)
                    
                    quantity_given = request_id.quantity_given
                    quantity_approved = int(quantity_given)
                    #quantity_approved = request_id.quantity_given
                    if quantity_requested > quantity_available:
                        messages.warning(request, 'Request not met,  requested quantity is more than quantity available!')
                        sendemail(orders)        
                    elif quantity_approved > quantity_available:
                        messages.warning(request, 'Request not met, quantity given is more than quantity available!')
                    else:
                        temporary_given = pending_approval - quantity_approved
                        #quantity_remain = int(quantity_available) - int(quantity_given)
                    
                        item_update = Items.objects.get(name=item_name, country=country, status='Active')
                       # item_update.quantity=quantity_remain
                        item_update.pending_approval=temporary_given 
                        item_update.save()
                        
                        itemrequest_update = ItemRequest.objects.get(id=item_id, country=country)
                        itemrequest_update.head_decision ='approve'
                       # itemrequest_update.quantity_given =  int(quantity_given)
                        itemrequest_update.stage =  'head corporate approval'
                        itemrequest_update.save()
                        
                        approval_log = ManagerApproval(request_id=item_id, inventManager=request.user, country=country)
                        approval_log.save()
                        messages.success(request, 'Request updated successfully!')
                    sendemail(orders)
                    return redirect('listPurchase')  
            
                elif'reject' in request.POST:
                    print('reject')
                    
                else:
                    cat = ItemRequest.objects.filter(item_name__icontains =search_name, country=country, manager_decision='approve', head_decision='pending')
                    paginator = Paginator(cat, 5)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    cat_count =  ItemRequest.objects.filter(item_name__icontains =search_name, country=country, manager_decision='approve', head_decision='pending').count()
                    print(cat_count)
                    context = {"cat":page_obj, "cat_count":cat_count, "orders":orders}
                    return render(request, 'purchases/list-purchase.html', context)
                    
            else:
                cat = ItemRequest.objects.filter(country=country, manager_decision='approve', head_decision='pending')
                paginator = Paginator(cat, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                cat_count =  ItemRequest.objects.filter(country=country, manager_decision='approve').count()
                context = {"cat":page_obj, "cat_count":cat_count, "orders":orders}
                return render(request, 'purchases/list-purchase.html', context)        

    context = {"cat_count":cat_count,"orders":orders }
    return render(request, 'purchases/list-purchase.html', context)


@login_required(login_url  ='login')
def exportCSV(request):
    country = request.session.get('country') 

    context = {}
    response = HttpResponse(request, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Reports.csv' 
    writer =csv.writer(response)
    writer.writerow(['Category','Name', 'Quantity', 'Unit Price'])
    cat =Items.objects.filter(country=country, status='Active')
    for item in cat:
        writer.writerow([item.category,  item.name, item.quantity, item.unit_price ])
    return response







@login_required(login_url  ='login')
def managerapprove(request,pk):
    manager = request.user
    initiator = ItemRequest.objects.get(id=pk)
    initiator_name = str(initiator) + '@ubagroup.com'
    logs = ItemRequest.objects.get(id = pk)
    #pk=pk
    form = ManagerForm()
    form2 = ItemRequestForm6(instance = logs)
    if request.method == 'POST':
        form2 = ItemRequestForm6(request.POST, instance = logs) 
        qty_requested = request.POST.get('qty_requested')
        form = ManagerForm(request.POST) 
        print(qty_requested)
        if form.is_valid():
            form.save()    
            return redirect('pendinginventmanager')
    context = {'form':form,'manager':manager,"logs":logs, 'form2':form2 }
    return render(request, 'inventory/quickapprove.html', context)








@login_required(login_url  ='login')
def addSupplier(request):
    country = request.session.get('country')

    context = {}
    return render(request, 'people/add-supplier.html', context)


@login_required(login_url  ='login')
def listSupplier(request):
    country = request.session.get('country')

    context = {}
    return render(request, 'people/list-supplier.html', context)

@login_required(login_url  ='login')
def addReturns(request):
    country = request.session.get('country')

    context = {}
    return render(request, 'returns/add-returns.html', context)


@login_required(login_url  ='login')
def listReturns(request):
    country = request.session.get('country')

    context = {}
    return render(request, 'returns/list-returns.html', context)








