from django.shortcuts import render,redirect
from .forms import (LoginForm,UpdateProfileForm,UpdateUserForm,Order_Form,
                    UserCreationForm,CreationForm,CameraManForm,CleintForm)
from .models import profile,CameraMan,Client,Order 
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView,UpdateView,DeleteView)
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator


#password change
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

"""
Use authenticate() function to verify a user by username and password.
Use login() function to log a user in.
Use logout() function to log a user out.
Use request.user.is_authenticated to check if the current user is authenticated.
User @login_required decorator to protect pages from unauthenticated users."""


def error_404_view(request, exception):
    return render(request,'404.html')

@login_required
def home(request):
   return render(request,'home.html')


#log in request 
def lin(request):
    if request.method == 'GET':
        form =LoginForm()
        context={'form':form}
        return render (request,'login.html',context)
    elif request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('home')
            else:
                 messages.error(request,f'Invalid username or password')
                 return redirect('login')
                

#log out
def sign_out(request):
    logout(request)
    messages.success(request,f'Good bye')
    return redirect('login')


#change password
@login_required
def change_password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user) #important
            messages.success(request,f'password has been changed')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request,'change_password.html',{'form':form})
        
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })    


#user profile 
@login_required
def profile_view(request):
    form = profile
    context = {
        'form' : form
    }

    return render(request,'profile.html',context)



#update
@login_required
def UserUpdate(request):
    if request.method == 'POST':
        model = profile
        ProfileForm = UpdateProfileForm(request.POST, instance=request.user)
        UserForm = UpdateUserForm(request.POST,request.FILES, instance=request.user.profile)
        if ProfileForm.is_valid() and UserForm.is_valid():
            ProfileForm.save()
            UserForm.save()
            messages.success(request,'profile updated')
            return redirect(to='users-profile')
        else:
            ProfileForm = UpdateProfileForm(instance=request.user.profile)
            UserForm = UpdateUserForm(instance=request.user)
    else:
        ProfileForm = UpdateProfileForm
        UserForm = UpdateUserForm
        context = {
            'user_form': UserForm,
            'profile_form': ProfileForm
        }
        return render(request,'profileupdate.html',context) 
@login_required    
def user_View(request):
    form = User.objects.all
    return render(request,'users.html',{'form':form})           
@login_required
def UserRegistration(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'user added')
            return redirect('/home')
            
        else:
            
            form = CreationForm
            messages.error(request,'try again')
            return render(request,'registration.html',{'form':form})

    else:
        form = CreationForm
        return render(request,'registration.html',{'form':form})
#################################Cameramane Section###############################
#cameraman View
@login_required
def CamerManView(request):
    form = CameraMan.objects.all()
    context = {
        'form':form,
    }
    return render(request,'cameraman.html',context)

#add camera man
@login_required
def AddCameraMan(request):
    form = CameraManForm
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = CameraManForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/cm/')
    else:
        return render(request,'addcm.html',context)
@method_decorator(login_required , name='dispatch')          
class cm_detail(DetailView):
    
    model = CameraMan
    template_name='cm_detail.html'
    context_object_name = 'form'
    def delete(request):
        form = CameraMan
        if request.method == 'POST':
            form = CameraMan(request.POST)
            form.delete()
            return redirect('')
        return render(request,'cameraman.html',{'form':form})

@method_decorator(login_required , name='dispatch')
class cm_update(UpdateView):
    model = CameraMan
    template_name = 'cm_update.html'
    context_object_name = 'form'
    fields = ['id','name','phone','email','kind']
    success_url = '/cm'
    def update(request):
        if request.method == 'POST':
            form=CameraMan(request.post)
            form.is_vaild()
            form.save()
            return redirect('http://127.0.0.1:8000/cm')
        
        else:
            return redirect('')
@method_decorator(login_required , name='dispatch')
class cm_Delete(DeleteView):
    model = CameraMan
    context_object_name = 'form'
    success_url = '/cm'        
###################################client Section################################################################
@login_required
def Client_View(request):
    form = Client.objects.all
    return render(request,'client.html',{'form':form})

@login_required
def cleint_add(request):
    form = CleintForm
    context = {
        'form':form
    }
    
    if request.method == 'POST':
        form = CleintForm(request.POST)
        
        form.save()
        return redirect('/client/')
    else:
        form = CleintForm
        context = {
            'form':form
        }  
        return render(request,'cleint_add.html',context)   

@method_decorator(login_required , name='dispatch')
class client_detail(DetailView):
    model = Client
    context_object_name = 'form'
    template_name = 'client_detail.html'

@method_decorator(login_required , name='dispatch')
class client_update(UpdateView):
    model = Client
    form = CleintForm
    context_object_name = 'form'
    template_name = 'client_update.html'
    fields = ['name','phone','email']
    success_url = '/client/'    


@method_decorator(login_required , name='dispatch')
class Client_Delete(DeleteView):
    model = Client
    context_object_name = 'form'
    template_object_name = 'test.html'
    success_url = '/client/'


################################orders####################################
@login_required
def Order_view (request):
    if User.is_superuser:
        form = Order.objects.all().values()
        context = {
        'form':form
    }
        return render(request,'order.html',context)
    else:
          form = Order.objects.all().values().filter(is_active=True)
          context = {
                'form':form
            }
          return render(request,'order.html',context)

@login_required
def Order_Add(request):
    form = Order_Form
    context = {
        'form':form
    }
    
    if request.method == 'POST':
        form = Order_Form(request.POST)
        form.save()
        return redirect('/order/')
        
    else:
        form = Order_Form
        context = {
            'form':form
        }  
        return render(request,'order_add.html',context) 


@method_decorator(login_required , name='dispatch')
class order_detail(DetailView):
    model = Order
    context_object_name = 'form'
    template_name = 'order_detail.html'


@method_decorator(login_required , name='dispatch')
class order_update(UpdateView):
    model = Order
    form = Order_Form
    context_object_name = 'form'
    template_name = 'order_update.html'
    fields = ['name','camera_men','location','client','created_by']
    success_url = '/order/'    



@method_decorator(login_required , name='dispatch')
class order_Delete(DeleteView):
    model = Order
    context_object_name = 'form'
    template_object_name = 'order_delete.html'
    success_url = '/order'  
    
      
@login_required    
def admin_approval(request):
    form = Order.objects.all().values().filter(is_active=False)
    context = {
        'form':form
    }

    return render(request,'admin_approval.html',context)     
