from django.shortcuts import render, redirect, get_object_or_404
import uuid
from django.views import View
from django.utils import timezone
from django.http import JsonResponse
from .models import Product, Brand, Category, SubCategory, Vendor, SerialNumber

def add_product(request):
    vendors = Vendor.objects.all()
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('categories')
        subcategory_id = request.POST.get('subcategories')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        model_name = request.POST.get('model_name')
        description = request.POST.get('description')
        serial_number = request.POST.get('serial_number')


        # Handle Vendor
        if vendor_id is None:
            msg = 'you must select or add vendor'
            return render(request, 'inventory.html', {'msg':msg, 'vendors': vendors})
        else:
            if vendor_id == 'new_vendor':
                vendor_name = request.POST.get('vendor_name')
                if vendor_name:
                    vendor = Vendor.objects.get_or_create(vendor_name=vendor_name)
                    return redirect('add_product')
                else:
                    msg = 'you must enter vendor name'
                    return render(request, 'inventory.html', {'msg':msg})
            else:
                vendor = get_object_or_404(Vendor, id=vendor_id)
                

        # Handle Brand
        if brand_id is None:
            msg = 'you must select or add brand'
            return render(request, 'inventory.html', {'msg':msg, 'vendors': vendors})
        else:
            if brand_id == 'new_brand':
                brand_name = request.POST.get('brand_name')
                if brand_name:
                    brand = Brand.objects.get_or_create(brand_name=brand_name, vendor=vendor)
                    return redirect('add_product')
                else:
                    msg = 'you must enter brand name'
                    return render(request, 'inventory.html', {'msg':msg})
            else:
                brand = get_object_or_404(Brand, id=brand_id)
                
        

        # Handle Category
        if category_id is None:
            msg = 'you must select or add category'
            return render(request, 'inventory.html', {'msg':msg, 'vendors': vendors})
        else:        
            if category_id == 'new_category':
                category_name = request.POST.get('category_name')
                if category_name:                
                    category = Category.objects.get_or_create(category_name=category_name, brand=brand)
                    return redirect('add_product')
                else:
                    msg = 'you must enter Category name'
                    return render(request, 'inventory.html', {'msg':msg})            
            else:
                category = get_object_or_404(Category, id=category_id)            
            

        # Handle Subcategory
        if subcategory_id is None:
            msg = 'you must select or add vendor'
            return render(request, 'inventory.html', {'msg':msg, 'vendors': vendors})
        else:
            if subcategory_id == 'new_subcategory':
                subcategory_name = request.POST.get('new_subcategory')
                if subcategory_name:
                    subcategory = SubCategory.objects.get_or_create(subcategory_name=subcategory_name, category=category)
                    return redirect('add_product')
                else:
                    msg = 'you must enter SubCategory name'
                    return render(request, 'inventory.html', {'msg':msg}) 
            else:
                subcategory = get_object_or_404(SubCategory, id=subcategory_id)

        product = Product.objects.create(
            name = product_name,
            description = description,
            price = price,
            model_name = model_name,
            vendor = vendor,
            brand = brand,
            category = category,
            subcategory = subcategory
        )
        if serial_number:
            serial_numbers = serial_number.split(",", " ")
            for serial_num in serial_numbers:
                sn = SerialNumber.objects.create(
                    serial_number = serial_num,
                    product = product, 
                    in_date = timezone.now().date()
                )
    

    return render(request, 'inventory.html', {'vendors': vendors})

def viewproduct(request):
    products = Product.objects.all()

    product_info_list = []

    for product in products:
        serial_numbers = SerialNumber.objects.filter(product=product)
        p_count = serial_numbers.count()
        product_info = {
            'product_name': product.name,
            'product_description': product.description,
            'vendor': product.vendor.vendor_name,  # Accessing vendor name through the product
            'count': p_count,
            'serial_numbers': serial_numbers,
            'serial_number_count': p_count,
        }
        product_info_list.append(product_info)

    context = {
        'product_info_list': product_info_list,
    }

    return render(request, 'viewproduct.html', context)

@staticmethod
def generate_serial_numbers():
    serial_numbers = str(uuid.uuid4())[:8]
    return serial_numbers

def get_brands(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    brands = Brand.objects.filter(vendor=vendor).values('id', 'brand_name')
    return JsonResponse(list(brands), safe=False)

def get_categories(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    categories = Category.objects.filter(brand=brand)
    data = [{'id': category.id, 'category_name': category.category_name} for category in categories]
    return JsonResponse(data, safe=False)
        
def get_subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    data = [{'id': subcategory.id, 'subcategory_name': subcategory.subcategory_name} for subcategory in subcategories]
    return JsonResponse(data, safe=False)







