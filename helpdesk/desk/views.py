from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# from .models import User
from django.contrib.auth.models import auth, User
# from .models import *
from .forms import *
# password - admin admin
# Create your views here.


def index(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    if request.user.is_authenticated:
        return redirect('user_panel')
    return render(request, "index.html")


def register(request):
    if request.user.is_authenticated:
        return redirect('user_panel')
    if request.method == 'POST':
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        user_name = request.POST['uname']
        password = request.POST['pwd']
        password1 = request.POST['pwd1']
        if password == password1:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'username already taken, try another!')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=f_name, last_name=l_name, username=user_name, password=password)
                user.save()
                messages.info(request, 'Successfully registered: Login now!')
                return redirect('login')
        else:
            messages.info(request, 'password do not match, try again!')
            return redirect('register')
    else:
        return render(request, "register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect('user_panel')
    if request.method == "POST":
        username = request.POST['un']
        password = request.POST['pswd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('user_panel')
        elif not User.objects.filter(username=username).exists():
            messages.info(request, 'User not registered, register here!')
            return redirect('register')
        else:
            messages.info(request, 'Error: Invalid Credentials!')
            return redirect('login')
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('index')


def admin_login(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    elif request.method == "POST":
        uname = request.POST['un1']
        pwd = request.POST['pswd1']
        user = auth.authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                auth.login(request, user)
                messages.info(request, 'Successfully Logged In')
                return redirect('admin_panel')
        except:
            messages.info(request, "invalid credentials!")
            return redirect('admin_login')
    else:
        return render(request, 'admin_login.html')


def admin_panel(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    query = Query.objects.all().order_by('published_date')
    x = {'query': query}
    return render(request, 'admin_panel.html', x)


def edit_query(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    query = get_object_or_404(Query, pk=pk)
    sts = query.status
    feed = query.feedback
    if sts == 'completed' and feed == 'positive':
        messages.success(request, 'query is resolved !')
        return redirect('admin_panel')
    if request.method == 'POST':
        form = QueryFrom(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = QueryFrom(instance=query)
    return render(request, 'edit_query.html', {'form': form})


def create_query(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = NewQuery(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.name = request.user
            query.published_date = timezone.now()
            query.save()
            return redirect('user_panel')
        else:
            form = NewQuery()
        return render(request, 'new_query.html', {'form': form})
    form = NewQuery()
    return render(request, 'new_query.html', {'form': form})


def user_panel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    query = Query.objects.filter(name=request.user)
    x = {'query': query}
    return render(request, 'user_panel.html', x)


def edit_user_query(request, pk):
    query = get_object_or_404(Query, pk=pk)
    sts = query.status
    feed = query.feedback
    if sts == 'completed' and feed == 'none':
        messages.error(request, "Query is resolved,Give feedback!")
        return redirect('feedback', pk)
    if sts == 'completed' and feed == 'positive':
        messages.success(request, "Query is solved !")
        return redirect('user_panel')
    if sts == 'completed' and feed == 'negative':
        query.status = 'not completed'
        query.feedback = 'none'
        query.save()
        return redirect('user_panel')
    if request.method == 'POST':
        form = NewQuery(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect('user_panel')
    else:
        form = NewQuery(instance=query)
    return render(request, 'edit_user_query.html', {'form': form})


def feedback(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    query = get_object_or_404(Query, pk=pk)
    if request.method == 'POST':
        form = Feedback(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect('user_panel')
    else:
        form = Feedback(instance=query)
    return render(request, 'feedback.html', {'form': form})

