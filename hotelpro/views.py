from django.shortcuts import render,redirect,HttpResponse
from hotelpro.models import  Packages , Employee_designation , Employee , food_category , Food , Room , Customer , Booking
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):
    r1=Room.objects.get(room_id='1')
    r2=Room.objects.get(room_id='2')
    r3=Room.objects.get(room_id='3')
    return render(request,'1index.html' , {'room1':r1 ,'room2':r2 , 'room3':r3})

def aboutus(request):
    return render(request, '2about.html')

def gallery(request):
    return render(request, '3gallery.html')

def contact(request):
    return render(request , '4contact.html')

# search rooms
def ourroomr(request , data):
    
    if data == 'Royal' :
        print(data)
        r=Room.objects.filter(room_type__icontains = 'Royal').exclude(room_type__icontains='Super Royal')
    elif data == 'SRoyal':
        r = Room.objects.filter(room_type__icontains='Super Royal')

    elif data == 'Gold':
        r = Room.objects.filter(room_type__icontains='Gold')
    elif data == 'All':
        r =  Room.objects.all()    

    return render(request , '5room.html' , {'Room' : r})
 
#  display room
def ourroom(request ):
    r=Room.objects.all()
    return render(request , '5room.html' , {'Room' : r})

def roomDetail(request , room_id):
    if request.session.get('customer') == None:
        return redirect('/cus_login')
    rd=Room.objects.get(room_id=room_id)

    return render(request , '6roomdetail.html' , {'rdetail' : rd } )

def count_number_of_day(start_date_str,end_date_str):
    if start_date_str and end_date_str:
        try:
                # Convert input strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                
                # Calculate the difference between the two dates
            difference = end_date - start_date
                
                # Extract the number of days from the difference
            number_of_days = difference.days
                
                # Do something with the number_of_days
                
            print("Number of days: {}".format(number_of_days))
            return number_of_days
        except ValueError:
            return messages.error("Invalid date format")
            
    else:
        return 0
        


def booknow(request , room_id ):
    if request.session.get('customer') == None:
        return redirect('/cus_login')
    rd=Room.objects.get(room_id=room_id)
    room_price=rd.room_price
    float(room_price)
    GST=(float(room_price)*12)/100
    final_total=float(room_price)+GST
    Day_price=0.0
    number_of_days=0
    total_amenities=0
    start_date_str = request.POST.get('check_in')
    end_date_str = request.POST.get('check_out')    

    if request.session.get('customer') == None:
        return redirect('/cus_login')

    customer_name = request.session.get('Customer.cus_name')
    print (customer_name)
    
    if request.method == 'POST':
        
        
        start_date_str = request.POST.get('check_in')
        end_date_str = request.POST.get('check_out')

        print(start_date_str)
        print(end_date_str)

        if start_date_str > end_date_str:

            print({room_id})
            return redirect(f"/booknow/{room_id}/")
            
        else:   
            number_of_days=count_number_of_day(start_date_str,end_date_str)

            rd=Room.objects.get(room_id=room_id)
            room_price=rd.room_price
            float(room_price)

            amenities=request.POST.getlist('Extra-Amenities')
            amenities_float = []
            for amenity in amenities:
                try:
                    amenity_float = float(amenity)
                    amenities_float.append(amenity_float)
                except ValueError:
                    pass
            
            total_amenities = sum(amenities_float)
            Day_price = number_of_days*float(room_price)
                
                
            GST=(Day_price*12)/100
            print(GST)
            
            final_total=total_amenities+GST+Day_price
            

            print(final_total)
        
    else:
        number_of_days=0

    if request.method=='POST':
        if request.POST.get('customer_name')  != None  :
            b=Booking()
            check_in=request.POST.get('check_in')
            
            b.Booking_cus_id=request.POST.get('customer_id')
            b.Booking_cus_name=request.POST.get('customer_name')
            b.Booking_cus_email=request.POST.get('customer_email')
            b.Booking_cus_mobileno=request.POST.get('customer_number')
            b.Booking_checkin=request.POST.get('check_in')
            b.Booking_checkout=request.POST.get('check_out')
            b.Booking_r_number=request.POST.get('room_id')
            b.Booking_r_type=request.POST.get('Room_type')
            b.Booking_totalprice=request.POST.get('final_total')
            room_number=request.POST.get('room_id')
            room_type=request.POST.get('Room_type')
            check_in=request.POST.get('check_in')
            check_out=request.POST.get('check_out')

            a=check_avail(room_number,room_type,check_in,check_out)
            print(a)

            if a :
                print("not")
                messages.error(request,"We regret to inform you that this room is unavailable on the date of your preference.")
                return redirect(f'/booknow/{room_id}')
               
            else :
                print("yes")
                b.save()
                cid=request.POST.get('customer_id')
                return redirect(f'/my_reservation/{cid}')
                
        
    return render(request , '7booknow.html' , { 'rdetail' : rd , 
                                                'final_total': final_total , 
                                                'GST':GST,
                                                'total_amenities':total_amenities,
                                                'number_of_days':number_of_days,
                                                'Day_price':Day_price,
                                                'start_date_str':start_date_str,
                                                'end_date_str':end_date_str })

def profile(request , cus_id):
    profile=Customer.objects.get(cus_id=cus_id)
    return render(request ,'8profile.html',{'pd' : profile})

def updateprofile(request , cus_id):
    customer=request.session.get('customer')
    if request.method == 'POST':
        s=Customer()
        s.cus_id=cus_id
        s.cus_name=request.POST.get('name')
        s.cus_email=request.POST.get('email')
        s.cus_password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        if s.cus_password != repassword:
            messages.error(request,'Password Mismatched')
            return redirect(f'/updateprofile/{customer}')
        s.cus_gender=request.POST.get('gender')
        s.cus_mobileno=request.POST.get('contact')
        s.cus_address=request.POST.get('address')
        s.save()
        return redirect('/')
    stu=Customer.objects.get(cus_id=cus_id)
    a={'customer':stu}
    return render(request,'9updateprofile.html',a)

# display
def foodmenu(request):
    if request.session.get('customer') == None:
        return redirect('/cus_login')
    food=Food.objects.all()
    fc = food_category.objects.all()
    return render(request, '10food.html', {'food':food , 'fc': fc})

# search
def menu(request, f):
    if f == f:
        if f =='All':
            food = Food.objects.all()
        else:
            food = Food.objects.filter(f_type_id=f)

    fc = food_category.objects.all()
    return render(request, '10food.html', {'food': food, 'fc': fc})

def booking(request , cus_id):
    if request.session.get('customer') == None:
        return redirect('/cus_login')
   
    
    customer=request.session.get('customer')
    
    booking=Booking.objects.all()
    
    return render(request, '11booking.html' , {'booking': booking , 'customer' : customer , 'room' : room })

def check_avail(room_number,room_type,check_in,check_out):
    booking=Booking.objects.all()
    number=Booking.objects.filter(Booking_r_number=room_number)
    print(number)
    avail = []
    for number in number:
        print(number)
        avail=Booking.objects.filter(
                    Booking_r_number=room_number,
                    Booking_r_type=room_type,
                    Booking_checkout__gt=check_in,
                    Booking_checkin__lt=check_out)
        print(avail)
    return avail
    
def a_booking(request ):
    avail=None
    if request.method == "POST":
        
        room_number = request.POST.get('number')
        r=Booking.objects.filter(Booking_r_number=room_number)
        room_cin = request.POST.get('check_in')
        cin=Booking.objects.filter(Booking_checkin=room_cin)
        room_cout = request.POST.get('check_out')
        cout=Booking.objects.filter(Booking_checkout=room_cout)
        avail=Booking.objects.filter(Booking_r_number=room_number,Booking_checkout__gt=room_cin,Booking_checkin__lt=room_cout)

   
    booking=Booking.objects.all()
    
    
    return render(request, 'bookinglist.html' , {'booking': booking , 'avail':avail })

def update_b_status(request , booking_id):
    if request.method == 'POST':
        b=Booking()
        id=request.POST.get('booking_id')
        b=Booking.objects.get(Booking_id=id)
        b.Booking_id=request.POST.get('booking_id')
        b.Booking_status=request.POST.get('status')
        b.save()
        return redirect('/a_booking')
    else:
        b=Booking.objects.get(Booking_id=booking_id)
        a={'booking':b}
        return render(request,'bookingupdate.html',a)
    

def deletebooking(request,Booking_id):
    s=Booking.objects.get(Booking_id=Booking_id)
    print(s)
    
    customer=request.session.get('customer')
    print(customer)

    s.delete()

    return redirect(f'/my_reservation/{customer}')
        

@login_required(login_url="admin_login")
def custumAdmin(request):
    room=Room.objects.all()
    r_count=room.count()
    reservation=Booking.objects.all()
    res_count=reservation.count()
    customer=Customer.objects.all()
    cus_count=customer.count()
    avail=None
    status_type=None
    if request.method == "GET":
        print("start")
        S=request.GET.get('status')
        status_type=Booking.objects.filter(Booking_status=S)
        print(status_type)
        print("end")

    if request.method == "POST":
        room_number = request.POST.get('number')
        r=Booking.objects.filter(Booking_r_number=room_number)
        room_cin = request.POST.get('check_in')
        cin=Booking.objects.filter(Booking_checkin=room_cin)
        room_cout = request.POST.get('check_out')
        cout=Booking.objects.filter(Booking_checkout=room_cout)
        avail=Booking.objects.filter(Booking_r_number=room_number,Booking_checkout__gt=room_cin,Booking_checkin__lt=room_cout)
    return render(request , 'admin.html' , {'title':"Admin Panel" , 'r_count':r_count ,'res_count' :res_count , 'cus_count':cus_count, 'reservation':reservation , 'avail':avail ,'status_type':status_type})

def admin_logout(request):
    logout(request)
    request.session.clear()
    return redirect("/login_admin") 

def login_admin(request):
    if request.method == "POST":
        uname=request.POST.get('userName')
        password=request.POST.get('password')
        if not User.objects.filter(username=uname).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login_admin')
        user=authenticate(username=uname,password=password)
        if user is None:
            messages.error(request,"Invalid Password ")
            return redirect('/login_admin')
        else:
            login(request,user)
            return redirect('/customadmin')
    return render(request,'admin_login.html')

def cus_login(request):
   if request.method == "POST":
        email=request.POST.get('cname')
        password=request.POST.get('cpassword')
        # it's a variable which store data like email_id and password in a list form 
        ss=Customer.objects.filter(cus_email=email,cus_password=password)
        if not Customer.objects.filter(cus_email=email):
            messages.error(request,"Email Id Does Not exits")
            return redirect('/cus_login')
        if not Customer.objects.filter(cus_password=password):
            messages.error(request,'Password Are Wrong !')
            return redirect('/cus_login')
        if Customer.objects.filter(cus_email=email,cus_password=password):
            for i in ss:
                request.session['customer']=i.cus_id
            return redirect('/')
   return render(request,'0cuslogin.html')

def cuslogout(request):
    request.session.clear()
    return redirect("/cus_login/")   

def cus_registration(request):
    if request.method == "POST":
        id=request.POST.get('id')
        if Customer.objects.filter(cus_id=id):
            messages.error(request,'Id Already Exists')
            return redirect('/cus_registration')
        name=request.POST.get('name')
        email=request.POST.get('email')
        if Customer.objects.filter(cus_email=email):
            messages.error(request,'Enter a Valid Email Address!')
            return redirect('/cus_registration')
        gender=request.POST.get('gender')
        password=request.POST.get('password')
        # password = make_password(setpassword)
        repassword=request.POST.get('repassword')
        # harepassword=make_password(repassword)
        if password != repassword:
            messages.error(request,'Password Mismatched')
            return redirect('/cus_registration')
        mobileno=request.POST.get('no')
        address=request.POST.get('address')
        Customer.objects.create(cus_id=id,cus_name=name,cus_email=email,cus_password=password,cus_gender=gender,cus_mobileno=mobileno,cus_address=address)
        return redirect('/cus_login')
    return render(request ,'0cusreg.html')


def customerlist(request):
    c=Customer.objects.all()
    print(c)
    c_name=None
    if request.method == "GET":
        print("start")
        cn=request.GET.get('name')
        if cn is not None:
            c_name=Customer.objects.filter(cus_name__istartswith=cn)
            print(c_name)
    return render(request , 'custumerlist.html' , {'cus': c , 'c_name':c_name})

def packageform(request):
    if request.method=='POST':
        if request.POST.get('pack_type'):
            p=Packages()
            p.p_id=request.POST.get('pack_id')
            p.package_types=request.POST.get('pack_type')
            p.package_details=request.POST.get('pack_detail')
            p.price=request.POST.get('pack_price')
            p.save()
            return redirect('/packagelist')
    else:
        return render(request,'packageform.html')
    
def package_deletepost(request,delete_id):
    s=Packages.objects.get(p_id=delete_id)
    s.delete()
    return redirect('/packagelist')

def editpost(request,edit_id):
    if request.method == 'POST':
            p=Packages()
            id=request.POST.get('pack_id')
            p=Packages.objects.get(p_id=id)
            p.p_id=request.POST.get('pack_id')
            p.package_types=request.POST.get('pack_type')
            p.package_details=request.POST.get('pack_detail')
            p.price=request.POST.get('pack_price')
            p.save()
            return redirect('/packagelist')
    else:
        stu=Packages.objects.get(p_id=edit_id)
        a={'demo':stu}
        return render(request,'package_edit.html',a)
        
def packagelist(request):
    a=Packages.objects.all()
    return render(request , 'packagelist.html',{'pack':a , 'title':"Package"})

def employeeform(request):
    a=Employee_designation.objects.all()
    if request.method=="POST":
        if request.POST.get('e_name'):
            emp=Employee()
            
            emp.e_id=request.POST.get('e_id')
            emp.e_name=request.POST.get('e_name')
            emp.desig_id=request.POST.get('Designation')
            emp.contact=request.POST.get('contact')
            emp.d_o_b_field=request.POST.get('dob')
            emp.gender=request.POST.get('gender')
            emp.shift=request.POST.get('shift')
            emp.address=request.POST.get('address')
            emp.salary=request.POST.get('salary')
            emp.save()
            return redirect('/employeelist')
    else:
        return render(request , 'employeeform.html' , {'des':a })
    
def employeelist(request):
    e=Employee.objects.all()
    return render(request , 'employeelist.html' , {'emp' : e , 'title':"Employee"})

def deletepost(request,delete_id):
    s=Employee.objects.get(e_id=delete_id)
    s.delete()
    return redirect('/employeelist')

def emp_editpost(request,edit_id):
    d=Employee_designation.objects.all()
    if request.method == 'POST':
            emp=Employee()
            id=request.POST.get('e_id')
            emp=Employee.objects.get(e_id=id)

            emp.e_id=request.POST.get('e_id')
            emp.e_name=request.POST.get('e_name')
            emp.desig_id=request.POST.get('Designation')
            emp.contact=request.POST.get('contact')
            emp.d_o_b_field=request.POST.get('dob')
            emp.gender=request.POST.get('gender')
            emp.shift=request.POST.get('shift')
            emp.address=request.POST.get('address')
            emp.salary=request.POST.get('salary')
            emp.save()
            return redirect('/employeelist')
    else:
        stu=Employee.objects.get(e_id=edit_id)
        a={'emp':stu ,'Designation':d}
        return render(request,'employee_edit.html',a )
    
def food(request):
    a=food_category.objects.all()
    if request.method == 'POST':
        if request.POST.get('name'):
            f = Food()
            f.f_id = request.POST.get('id')
            f.f_name = request.POST.get('name')
            f.f_price = request.POST.get('price')
            f.f_type_id= request.POST.get('f_type')
            f.f_img=request.FILES.get('img')
            f.save()
            return redirect('/foodlist')
    else:
        return render(request , 'food.html',{'catagory':a})
    
def foodlist(request):
    f=Food.objects.all()
    name=None
    if request.method == "GET":
        print("start")
        fn=request.GET.get('name')
        if fn is not None:
            name=Food.objects.filter(f_name__istartswith=fn)
            print(name)
    return render( request , 'foodlist.html' , {'food':f , 'title':"Food" , "name":name})

def fe_editpost(request,edit_id):
    c=food_category.objects.all()
    
    if request.method == 'POST':
            p=Food()
            id=request.POST.get('id')
            p=Food.objects.get(f_id=id)
            p.f_id=request.POST.get('id')
            p.f_name=request.POST.get('name')
            p.f_type_id= request.POST.get('f_type')
            p.f_price=request.POST.get('price')
            p.f_img=request.FILES.get('img')
            p.save()
            return redirect('/foodlist')
    else:
        stu=Food.objects.get(f_id=edit_id)
        a={'demo':stu , 'food_categories':c} 
        return render(request,'food_edit.html' , a)
    
def f_deletepost(request,delete_id):
    s=Food.objects.get(f_id=delete_id)
    s.delete()
    return redirect('/foodlist')

def f_list(request):
    a=food_category.objects.all()
    return render(request,'food_categorylist.html',{'food':a , 'title':"Food Category"})

def f_category(request):
    if request.method == 'POST':
        if request.POST.get('Category_name'):
            fc=food_category()
            fc.fc_id=request.POST.get('Category_id')
            fc.fc_name=request.POST.get('Category_name')
            fc.save()
            return redirect("/food_categorylist")
    else:
        return render(request,'food_category.html')

def f_edit(request,edit_id):
    if request.method == 'POST':
        f=food_category()
        id=request.POST.get('Category_id')
        f=food_category.objects.get(fc_id=id)
        f.fc_id=request.POST.get('Category_id')
        f.fc_name=request.POST.get('Category_name')
        f.save()
        return redirect('/food_categorylist')
    else:
        data=food_category.objects.get(fc_id=edit_id)
        a={'demo':data} 
        return render(request,'food_categoryedit.html' , a)

def f_delete(request,delete_id):
    s=food_category.objects.get(fc_id=delete_id)
    s.delete()
    return redirect('/food_categorylist')

def designation(request):
    if request.method == 'POST':
        if request.POST.get('Designation_name'):
            d=Employee_designation()
            d.des_id=request.POST.get('Designation_id')
            d.des_name=request.POST.get('Designation_name')
            d.save()
            return redirect('/designationlist')
    else:
         return render(request , 'designation.html')
    
def designationlist(request):
    des=Employee_designation.objects.all()
    return render(request , 'designationlist.html' , {'desig':des , 'title':"Designation"})

def des_delete(retuest,delete_id):
    s=Employee_designation.objects.get(des_id=delete_id)
    s.delete()
    return redirect('/designationlist')

def designation_edit(request,edit_id):
    if request.method == 'POST':
        desig=Employee_designation()
        id=request.POST.get('Designation_id')
        desig=Employee_designation.objects.get(des_id=id)
        desig.des_id=request.POST.get('Designation_id')
        desig.des_name=request.POST.get('Designation_name')
        desig.save()
        return redirect('/designationlist')
    else:
        d=Employee_designation.objects.get(des_id=edit_id)
        return render(request , 'designationedit.html' , {'designation':d})

#insert room
def room(request):
    if request.method== 'POST' :
        if request.POST.get('r_name'):
            r=Room()
            r.room_id=request.POST.get('r_id')
            r.room_name=request.POST.get('r_name')
            r.room_descri=request.POST.get('r_detail')
            r.room_type=request.POST.get('r_type')
            r.room_price=request.POST.get('r_price')
            r.room_img=request.FILES.get('r_img')
            r.ac_price=request.POST.get('ac_price')
            r.extra_bed_price=request.POST.get('extra_bed_price')
            r.save()
            return redirect('/roomlist')
    else:
        return render(request, 'room.html')

#   display room  
def roomlist(request):
    get=Room.objects.all()   
    return render(request , 'roomlist.html' , {'r':get , 'title':"Room" } )

# delete room
def r_deletepost(request,delete_id):
    s=Room.objects.get(room_id=delete_id)
    s.delete()
    return redirect('/roomlist')

# edit room
def r_editpost(request , edit_id):
    if request.method == 'POST':
        r=Room()
        id=request.POST.get('r_id')
        r=Room.objects.get(room_id=id)
        r.room_id=request.POST.get('r_id')
        r.room_name=request.POST.get('r_name')
        r.room_descri=request.POST.get('r_detail')
        r.room_type=request.POST.get('r_type')
        r.room_price=request.POST.get('r_price')
        r.room_img=request.FILES.get('r_img')
        r.ac_price=request.POST.get('ac_price')
        r.extra_bed_price=request.POST.get('extra_bed_price')
        r.save()
        return redirect('/roomlist')
    else:
        d=Room.objects.get(room_id=edit_id)
        return render(request , 'roomedit.html' , {'room':d})       