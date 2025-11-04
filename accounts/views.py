from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('accounts:signup')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/signup.html',{'is_logged_in':request.user.is_authenticated})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('accounts:login')

from django.db import connection
from core.models import Herb

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT h.id, h.name, h.image_url
            FROM core_herb h
            JOIN herbocare_herb_favorited_by f ON h.id = f.herb_id
            WHERE f.user_id = %s
        """, [user_id])
        rows = cursor.fetchall()

    favorites = [{'id': row[0], 'name': row[1], 'image_url': row[2]} for row in rows]

    return render(request, 'accounts/dashboard.html', {'favorites': favorites})




from .models import Herb, Favorite
from django.contrib.auth.decorators import login_required

# @login_required
# def add_to_favorites(request, herb_id):
#     herb = Herb.objects.get(id=herb_id)
#     favorite, created = Favorite.objects.get_or_create(user=request.user, herb=herb)
#     if not created:
#         messages.info(request, "Already in your favorites.")
#     else:
#         messages.success(request, "Added to favorites.")
#     return redirect('home')

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection

from core.models import Herb  # لو Herb موجود في app core

@login_required
def add_to_favorites(request, herb_id):
    herb = get_object_or_404(Herb, id=herb_id)
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO herbocare_herb_favorited_by (herb_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, [herb.id, user_id])

    return redirect('recommend')  # أو رجعي لنفس الصفحة

from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def remove_from_favorites(request, herb_id):
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM herbocare_herb_favorited_by
            WHERE herb_id = %s AND user_id = %s
        """, [herb_id, user_id])

    return redirect('accounts:dashboard')
