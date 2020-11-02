from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ProfileUser
import random
from django.core.mail import send_mail
# Create your views here.


class Login(View):
    def get(self, request):
        return render(request, 'account/login/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user.is_authenticated)
        if user.is_authenticated:
            if user.is_active:
                login(request, user)

        return redirect('shop:index')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class Account(LoginRequiredMixin, View):
    login_url = 'acoount:login'

    def get(self, request):
        return render(request, 'account/account.html')


class ChangePassword(View):
    def get(self, request):
        return render(request, 'account/change_password/changepassword.html')

    def post(self, request):
        pass1 = request.POST['password1']
        pass2 = request.POST['password1']
        if pass1 == pass2:
            user = User.objects.get(username=request.user.username)
            user.set_password(pass2)
            user.save()
            messages.success(request, 'Đổi mật khẩu thành công')
        else:
            messages.error(request, 'chưa đổi thành công')
        return render(request, 'account/change_password/changepassword.html')


class RegisterUser(View):
    def get(self, request):
        return render(request, 'account/registration/register.html')

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        gender = request.POST['sex']
        birthday = '-'.join(list(reversed(request.POST.getlist('birthday'))))
        new_user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        if password1 == password2:
            new_user.set_password(password2)
            new_user.save()
            profile = ProfileUser.objects.create(user=new_user, gender=gender, birthday=birthday)
            profile.save()
            messages.success(request, 'Tạo tài khoản thành công, Xin mời đăng nhập')
        return redirect('account:login')


class ResetPassword(View):
    def get(self, request):
        return render(request, 'account/reset_password/reset_pass.html')

    def sen_mail_reset_pass(self, pass_defaul):
        pass

    def post(self, request):
        # lấy mail post
        mail = request.POST['email']
        # lấy đối tượng user thông qua mail
        user = get_object_or_404(User, email=mail)
        if user:
            # tạo 1 mật khẩu random
            pass_defaul = random.randint(100000, 9999999)
            print(pass_defaul)
            # set_password mới cho user
            user.set_password(str(pass_defaul))
            user.save()
            # gửi mail pass mới cho kh
            subject = f'mật khẩu reset của user: {user.username}'
            message = f'mật khẩu: {pass_defaul} - đổi mật khẩu này sau khi đăng nhập'
            send_mail(subject, message, 'tuantt1889@gmail.com', [mail])
            messages.success(request, 'bạn vui lòng kiểm tra email để nhận mật khẩu')
        return redirect('account:login')