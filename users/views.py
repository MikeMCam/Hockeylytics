from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, UserTypeForm
from django.contrib.auth.decorators import login_required


# Form for registration page
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        type_form = UserTypeForm(request.POST)
        if form.is_valid() and type_form.is_valid():
            # Need to do it this way to create the profile instance
            user = form.save()
            user.refresh_from_db()
            profile_form = UserTypeForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            messages.success(request, f'Your account has been created! Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        type_form = UserTypeForm()

    context = {
        'form': form,
        'type_form': type_form,
    }
    return render(request, 'users/register.html', context)


# Form for updating profile
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/profile.html', context)
