from django.shortcuts import render,redirect
from user.forms import UserRegistrationForm,UserLoginForm,ForgotPasswordForm,OTPForm,ResetPasswordForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import random
from user.models import UserProfile, AllLogin
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login, logout

# User authentication
def LoginPage(Request):
    if Request.method=='GET':
        if Request.user.is_authenticated: # if user has already logged in
            current_user=Request.user
            return redirect('/chat/lobby/?name=lobby&user='+str(current_user)) # redirect to chat interface
        else:
            Login=UserLoginForm(Request.GET) # get username and password from form
            if Login.is_valid(): # if all fields are not empty 
                Username = Login.cleaned_data['UserID']
                Password=Login.cleaned_data['Password']
                # authenticate user using JWT token (over HTTP using REST API)
                user = authenticate(Request, username=Username, password=Password)
                if user is not None:
                    # only allow one user to login at once from one client
                        login(Request, user) # credentials are valid and login user
                        try:
                            print(Request.user)
                            AllLogin.objects.get(user= Request.user) # checkif user already logged in
                            messages.error(Request,'Already Logged In') # show warning message
                            logout(Request) # logout user
                        except AllLogin.DoesNotExist:
                            AllLogin.objects.create(user= Request.user) # update database for user logged in
                            return redirect('/chat/lobby/?name=lobby&user='+Username) # redirect to chat interface
                else:
                    messages.error(Request,'Account Doesnt Exist! Try Creating One.') # show warning message
            else: # credentials are not valid
                Login=UserLoginForm()
    return render(Request,'Login.html',{'title':'Login'})

# logout user
def LogOut(request):
    if request.user.is_authenticated: # if anyone has logged in
        AllLogin.objects.filter(user= request.user).delete() # delete user from database
        logout(request) # logout user
    return render(request,'Login.html',{'title':'Login'})

# SignUp as a new user
def SignUpPage(Request):
    if Request.method == "POST":
        SignUp = UserRegistrationForm(Request.POST) # get username, email, password from form
        if SignUp.is_valid(): # if all fields are not empty 
            UserID = SignUp.cleaned_data['UserID']
            Email=SignUp.cleaned_data['Email']
            Password=SignUp.cleaned_data['Password']
            RetypePassword=SignUp.cleaned_data['RetypePassword']
            if UserProfile.objects.filter(Q(username=UserID) | Q(email=Email)).exists(): # user with same email or username already exist
                messages.error(Request,"User Name or Email has already been taken. Please try another")
            else:
                if Password!=RetypePassword: # password and confirm password are not same
                    messages.error(Request, "Passwords Do Not Match!.")
                else:
                    user = UserProfile.objects.create_user(username=UserID, email=Email) # create new user with username and email
                    user.set_password(Password) # set password for new user
                    user.save() # save changes
                    # generate token for user
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response = {'token':token}
                    print(response)
                    messages.success(Request, f"Hey, {UserID}!") # show success message
                    return redirect('Login') # redirect to login page
        else:
            SignUp = UserRegistrationForm()
    return render(Request,'Signup.html',{'title':'SignUp'})

ResetPassword={} # contains email and OTP

def ForgotPasswordPage(Request):
    if Request.method=='GET':
        ForgotPassword=ForgotPasswordForm(Request.GET) # get email from form
        if ForgotPassword.is_valid(): # if all fields are not empty
            Email=ForgotPassword.cleaned_data['Email'] # email
            try:
                user=UserProfile.objects.get(email=Email) # get user with email from database
                # if user with email exist
                O_T_P = str(random.randint(1000,9999)) # generate OTP in range from 1000 - 9999
                ResetPassword[Email]=O_T_P # store OTP with respective email
                messageContent=f'Hi,\n      We got a Request to Reset your InstaChat Password.\n    Your OTP is {O_T_P}. If you Ignore this message your Password will not be Changed. '
                msg = EmailMessage('InstaChat - Password Reset', messageContent,settings.EMAIL_HOST_USER,[Email])
                msg.send() # send email
                messages.success(Request, f"OTP Sent to Your Mail ID !") # show success message
                return redirect('Otp') # redirect to OTP page
            except UserProfile.DoesNotExist: # if no user with email exists
                messages.error(Request,"Un-Registered Email ID !") # show warning message
        else: # if any fields are empty 
            ForgotPassword = ForgotPasswordForm()
    return render(Request,'ForgotPassword.html',{'title':'ForgotPassword'})

def OTPPage(Request):
    if Request.method=='GET':
        FormOTP=OTPForm(Request.GET) # get otp from form
        if FormOTP.is_valid(): # if all fields are not empty
            Otp=FormOTP.cleaned_data['Otp'] # OTP
            if Otp in ResetPassword.values(): # if OTP is same as sent in email
                return redirect('ResetPassword') # redirect to reset password page
            else: # if OTP is not same as sent in email
                messages.error(Request,"Invalid OTP!") # show warning message
        else: # if any fields are empty  
            FormOTP=OTPForm()
    return render(Request,'Otp.html',{'title':'Otp'})

# reset password
def ResetPasswordPage(Request):
    if Request.method=='POST':
        FormResetPassword=ResetPasswordForm(Request.POST) # get new password and confirmation new password
        if FormResetPassword.is_valid(): # if all fields are not empty
            newPassword=FormResetPassword.cleaned_data['newPassword'] # new password
            reTypeNewPassword=FormResetPassword.cleaned_data['reTypeNewPassword'] # confirmation new password
            EmailKey=list(ResetPassword.keys())[0] # get email to which OTP was sent
            if newPassword==reTypeNewPassword: # if new password and confirmation new password are same
                user=UserProfile.objects.get(email=EmailKey) # get user with email from database
                user.set_password(newPassword) # set new password for user
                user.save() # save the changes
                messages.success(Request,'Reset Password Successful !') # show success message
                return redirect('Login') # redirect to login page
            elif newPassword!=reTypeNewPassword: # if new password and confirmation new password are not same
                messages.error(Request,'Passwords do not Match !') # show warning message
        else: # if any fields are empty
            FormResetPassword=ResetPasswordForm()
    return render(Request,'ResetPassword.html',{'title':'Reset Password'})
