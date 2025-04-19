from django.db import models

# Create your models here.
class Packages(models.Model):
    p_id = models.AutoField(primary_key=True)
    package_types = models.CharField(db_column='package types', max_length=20) 
    package_details=models.TextField(max_length=800)
    price = models.IntegerField()


class Employee_designation(models.Model):
    des_id = models.AutoField(primary_key=True)
    des_name = models.CharField(max_length=50)

    def __str__(self):
        return self.des_name

class Employee(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=20)
    desig = models.ForeignKey(Employee_designation,on_delete=models.CASCADE,null=True)
    contact = models.IntegerField()
    d_o_b_field = models.DateField(db_column='D.O.B.')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    gender = models.CharField( max_length = 5) 
    shift = models.CharField(max_length=7)
    address = models.CharField(max_length=30)
    salary = models.IntegerField()

    def __str__(self):
        return self.e_name

class food_category(models.Model):
    fc_id=models.AutoField(primary_key=True)
    fc_name=models.CharField(max_length=30)

    def __str__(self):
        return self.fc_name

class Food(models.Model):
    f_id=models.AutoField(primary_key=True)
    f_name=models.CharField(max_length=255)
    f_price=models.DecimalField(max_digits=10,decimal_places=2)
    f_type=models.ForeignKey(food_category,on_delete=models.CASCADE,null=True)
    f_img=models.ImageField(upload_to='upload/')

class Room(models.Model):
    room_id=models.AutoField(primary_key=True)
    room_img=models.ImageField(upload_to='upload/')
    room_name=models.CharField(max_length=100)
    room_descri=models.TextField(max_length=500)
    room_type=models.CharField(max_length=10)
    room_price=models.DecimalField(max_digits=10,decimal_places=2)
    ac_price=models.DecimalField(max_digits=10,decimal_places=2)
    extra_bed_price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return self.room_type
    
        
    
class Customer(models.Model):
    cus_id = models.IntegerField(primary_key=True)
    cus_name = models.CharField(max_length=25)
    cus_email = models.CharField(max_length=30)
    cus_password = models.CharField(max_length=16)
    cus_gender = models.CharField(max_length=10)
    cus_mobileno = models.BigIntegerField()
    cus_address = models.CharField(max_length=100)

    def __str__(self):
        return self.cus_name
    
class Booking(models.Model):
    Booking_id=models.AutoField(primary_key=True)
    Booking_cus_id=models.IntegerField()
    Booking_cus_name=models.CharField(max_length=40)
    Booking_cus_email=models.CharField(max_length=50)
    Booking_cus_mobileno = models.BigIntegerField()
    Booking_checkin=models.DateField()
    Booking_checkout=models.DateField()
    Booking_r_number=models.IntegerField()
    Booking_r_type=models.CharField(max_length=50)
    Booking_totalprice=models.FloatField()
    Booking_status=models.CharField(default='Pending Reservation',max_length=50)
