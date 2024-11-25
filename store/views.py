from django.shortcuts import render, redirect
from django.views.generic import View
from store.forms import SignUpForm, LoginForm
from store.models import Product, User
from django.core.mail import send_mail
from twilio.rest import Client
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.



def send_otp_email(user):
    
    user.generate_otp()
    send_otp_phone(user.otp)
    subject = 'Verify your email'
    message = f'OTP for account verification is {user.otp}'
    from_email = 'iamrbn03@gmail.com'
    to_email = [user.email]
    
    send_mail(subject, message, from_email, to_email)


class SignUpView(View):
    
    template_name = 'register.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            
            user_obj.save()
            
            send_otp_email(user_obj)

            return redirect('verify-email')
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
        
        
class VerifyEmailView(View):

    template_name = 'verify_email.html'
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        
        otp = request.POST.get('otp')
        
        try:
            user_obj = User.objects.get(otp=otp)
        
            user_obj.is_active = True
            user_obj.is_verified = True
            user_obj.otp = None
            
            user_obj.save()
            return redirect('signup')
        
        except:
            
            messages.error(request, 'Invalid OTP')
            
            return render(request, self.template_name)
        
        
class SignInView(View):
    
    template_name = 'signin.html'
    form_class = LoginForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            
            user_obj = authenticate(request, username=uname, password=pwd)
            

            
            if user_obj:
                
                login(request, user_obj)
                return redirect('product-list')
            
        return render(request, self.template_name, {'form':form})
    
    
class ProductListView(View):
    
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        
        qs = Product.objects.all()
        
        context = {
            'products': qs
        }
        
        return render(request, self.template_name, context)
    
    
class ProductDetailView(View):
    
    template_name = 'product_detail.html'
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        product = Product.objects.get(id=id)
        
        context = {
            'product':product
        }

        return render(request, self.template_name, context)