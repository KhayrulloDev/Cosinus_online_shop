from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model

User = get_user_model()


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords are not same!')
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('/register')

        user = User.objects.create_user(
            username=username,
            password=confirm_password,
            first_name=first_name
        )
        return redirect('/')


class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('/users/login')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')
