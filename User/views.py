import csv
import os
from collections import defaultdict
from subprocess import call
from multiprocessing import Process, Queue
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Product, ScrapedCSV

from threading import Thread
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from .azani_spider import AzaniSpider, items
from twisted.internet import reactor


# Create your views here.
def index(request):
    return redirect('users:all_products')


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('users:all_products')
        form = LoginForm()
        return render(request, 'User/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('users:all_products')
            else:
                # return HttpResponse("Wrong Username or password")
                form = LoginForm()
                return render(request, 'User/login.html', {'form': form, 'error': 'Wrong Username or Password'})


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'User/registration.html', {'form': form})
    else:
        form = RegistrationForm(request.POST)
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect('users:login')


@login_required(login_url='users:login')
def profile(request):
    if request.user.is_authenticated():
        return render(request, 'User/profile.html', {'name': request.user.get_full_name()})
    else:
        return redirect('users:login')


@login_required(login_url='users:login')
def user_logout(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def generate_table(request):
    products = []
    columns = defaultdict(list)
    f = UploadedCSV.objects.all().order_by('-pk')[0]
    reader = csv.DictReader(f.csv_file)
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)
    for order_id, order_status, product_code, product_name, product_url, cost_price in zip(columns['order_id'],
                                                                                           columns['order_status'],
                                                                                           columns['product_code'],
                                                                                           columns['product_name'],
                                                                                           columns['product_url'],
                                                                                           columns['cost_price']):
        product = Product()
        product.order_id = order_id
        product.order_status = order_status
        product.product_name = product_name
        product.product_code = product_code
        product.product_url = product_url
        try:
            product.cost_price = float(cost_price)
        except ValueError as e:
            print(e)
        product.save()
    return redirect('users:all_products')


@login_required(login_url='users:login')
def upload_csv(request):
    if request.method == 'GET':
        form = UploadCSVForm()
        return render(request, 'User/upload_csv.html', {'form': form})
    else:
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('users:generate')


@login_required(login_url='users:login')
def all_products(request):
    if request.GET.get('order_by_status'):
        products = Product.objects.all().order_by('order_status')
        return render(request, 'User/tables.html', {'products': products, 'active_page': 2})
    elif request.GET.get('active_order'):
        products = Product.objects.filter(order_status='Active').order_by('-pk')
        return render(request, 'User/tables.html', {'products': products, 'active_page': 3})
    elif request.GET.get('cancelled_order'):
        products = Product.objects.filter(order_status='Cancelled').order_by('-pk')
        return render(request, 'User/tables.html', {'products': products, 'active_page': 4})
    else:
        products = Product.objects.all().order_by('-pk')
        return render(request, 'User/tables.html', {'products': products, 'active_page': 1})


@login_required(login_url='users:login')
def deploy_spider(request):
    if request.method == 'GET':
        if request.GET.get('text'):
            try:
                os.remove('User/export.csv')
            except OSError:
                print("Already Removed")
            thread = Thread(target=call(["scrapy", "runspider", "User/azani_spider.py"]))
            thread.start()
            thread.join()
            # call(["scrapy", "runspider", "User/azani_spider.py"])
            f = open("User/export.csv")
            scraped_csv = ScrapedCSV(csv_file=File(f))
            scraped_csv.save()
            return JsonResponse({
                'Response': "Success",
                'Data': ScrapedCSV.objects.all().order_by('-created_at')[0].csv_file.url
            })

    return render(request, 'User/spider_result.html')


@login_required(login_url='users:login')
def some_view(request):
    products = Product.objects.all().order_by('-pk')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All_Products.csv"'
    product_dict = product_objects_to_dict(products)
    keys = product_dict[0].keys()
    writer = csv.DictWriter(response, keys)
    writer.writeheader()
    writer.writerows(product_dict)

    # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response


def product_objects_to_dict(products):
    prodlist = []
    for product in products:
        prodlist.append({
            "Order Id": product.order_id,
            "Product Name": product.product_name,
            "Order Status": product.order_status,
            "Product Url": product.product_url,
            "Cost Price": product.cost_price
        })
    return prodlist


@login_required(login_url='users:login')
def create(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'User/create_product.html', {"form": form})
    else:
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:all_products')


def start_spider_debug(request):
    products = []
    q = Queue()
    p = Process(target=start_crawl, args=(q,))
    p.daemon = True
    p.start()
    products = q.get()
    print(products)
    p.join()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All_Products.csv"'
    product_dict = generate_scraped_object_array(products)
    keys = product_dict[0].keys()
    writer = csv.DictWriter(response, keys)
    writer.writeheader()
    writer.writerows(product_dict)
    return response


def start_crawl(q):
    print("Server Started")
    runner = CrawlerRunner()
    d = runner.crawl(AzaniSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=False)
    print("Scrape Completed")
    print(items)
    q.put(items)


def generate_scraped_object_array(products):
    prodlist = []
    for product in products:
        # if product.get("Product Name") is not None or product.get("Price") is not None or product.get(
        #         "Url") is not None or product.get('Description' is not None):
        prodlist.append({
            "Product Name": product.get('Product Name'),
            "Price": product.get('Price'),
            "Url": product.get('URL'),
            "Description": str(product.get('Description')),
        })

    return prodlist
