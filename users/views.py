from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .forms import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get('username')
            messages.success(request, f' Welcome to the open blog,{username}now you can Login')
            return redirect('/login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('post_list')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form ': p_form
    }
    return render(request, 'users/profile.html', context)


def other_profile(request,id):
    user = get_object_or_404(Profile, id=id)
    context = {'user':user}
    return render(request, 'users/other_profile.html', context)


def list_users(request):
    group = Group.objects.get(name='moder')
    if group in request.user.groups.all() and not request.user.profile.banned:
        users = Profile.objects.all()
    else:
        return redirect('forbidden')
    return render(request, 'users/list_users.html', {'users': users})


def banned_user(request, id):
    group = Group.objects.get(name='moder')
    if group in request.user.groups.all() and not request.user.profile.banned:
        user = get_object_or_404(Profile, id=id)
        if request.method == 'POST':
            form = ProfileBannedUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('list_users')
        else:
            form = ProfileBannedUserForm(instance=user)
    else:
        return redirect('forbidden')
    context = {
        'user': user,
        'form': form}
    return render(request, 'users/banned_user.html', context)

def give_moder(request, id):
    a_group = Group.objects.get(name='super_admin')
    group = Group.objects.get(name='moder')
    if a_group in request.user.groups.all():
        user = get_object_or_404(Profile, id=id)
        if request.method == 'POST':
            form = GiveModerUserForm(request.POST, instance=user)
            if form.is_valid():
                if user.is_moder:
                    user.user.groups.add(group)
                else:
                    user.user.groups.remove(group)
                form.save()
                return redirect('list_users')
        else:
            form = GiveModerUserForm(instance=user)
    else:
        return redirect('forbidden')
    context = {
        'user': user,
        'form': form}
    return render(request, 'users/give_moder.html', context)