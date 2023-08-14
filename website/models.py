from django.db import models
#user profile
from django.contrib.auth.models import User   #user profile
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from tinymce.models import HTMLField


class Phone(models.Model):
    '''
    Phone is the user Phone
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)

'''
By defult we have auth
class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=15)
'''
class Client(models.Model):
    '''
    Client in the company Client
    '''
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30,blank=True, null=True,unique=True)
    phone       = models.CharField(max_length=15)
    email       = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class CameraMan(models.Model):
    '''
    Order is a Camera Man working in the company
    '''
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30)
    phone       = models.CharField(max_length=15)
    email       = models.CharField(max_length=255, blank=True, null=True)
    kind        = models.CharField(max_length=30)
    date_joined = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    #b_day 

    
    def __str__(self):
        return self.name

    def WorkPresent(self):
        worked_for  = self.order_set.all().count()
        total_order = Order.objects.count()
        if not total_order == 0:
            present = worked_for / total_order * 100
        else: present = 1
        return present
        
    def last_order(self):
        return self.order_set.all().latest('date')

class WeekEnd(models.Model):
    id          = models.AutoField(primary_key=True)
    day         = models.CharField(max_length=30)
    cameraMan   = models.ForeignKey(CameraMan, on_delete=models.CASCADE)
    #created_by  = models.ForeignKey(User, related_name='created_by' ,on_delete=models.CASCADE)

'''
class WorkFor(models.Model):
    camera_men   = models.ForeignKey(CameraMan, null=True, on_delete=models.CASCADE)
    order       = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
'''

class Order(models.Model):
    '''
    Order is the working order for the camera man  
    '''
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30) 
    #cameraMan   = models.ForeignKey(CameraMan, null=True, on_delete=models.CASCADE)
    camera_men  = models.ManyToManyField(CameraMan)
    location    = models.CharField(max_length=15)
    #date        = models.DateField()
    client      = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_by  = models.ForeignKey(User, related_name='created_by' ,on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=False)
    status      = models.BooleanField(default=False)
    assigned_by = models.ForeignKey(User, null=True, related_name='assigned_by',on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
class PermissionIssuer(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    '''
    permission is the security_permission for the camera man to get Access to the work location 
    '''
    id         = models.AutoField(primary_key=True)
    cameraMan  = models.ForeignKey(CameraMan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date   = models.DateField()
    issuer     = models.ForeignKey(PermissionIssuer, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)

class VacationKind(models.Model):
    '''
    Is the Vacation Kind of a Camera Man
    '''
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Vacation(models.Model):
    '''
    Is the Vacation of a Camera Man
    '''
    id          = models.AutoField(primary_key=True)
    #kind        = models.CharField(max_length=20)
    end_date    = models.DateField()
    start_date  = models.DateField()
    cameraMan   = models.ForeignKey(CameraMan, on_delete=models.CASCADE)
    kind        = models.ForeignKey(VacationKind, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)



class Token(models.Model):
    code         = models.CharField(max_length=30)
    created_date = models.DateField(auto_now_add=True)
    invoked_date = models.DateField(null=True)
    is_active    = models.BooleanField(default=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.code


class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

"""
class client2(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30,blank=True,null=True,unique=True)
    phone       = models.CharField(max_length=15)
    email       = models.EmailField(max_length=50,blank=True,null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)
    created_by  =models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    

class CameraMan2(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    kind = models.CharField(max_length=30)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Salary2(models.Model):
    id                 = models.AutoField(primary_key=True)
    cameraman          = models.ForeignKey(CameraMan,on_delete=models.CASCADE)
    #order              = models.ForeignKey(order,on_delete=models.CASCADE)
    #kind               = models.ForeignKey(SalaryKind,on_delete=models.CASCADE)
    Created_by         = models.ForeignKey(User,on_delete=models.CASCADE)
    production_confirm = models.ForeignKey(User, null=True, related_name='production_confirm', on_delete=models.CASCADE)
    accountant_confirm = models.ForeignKey(User, null=True, related_name='accountant_confirm',on_delete=models.CASCADE)
    is_active          = models.BooleanField(default=True)
"""