from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import UserPassword
from .forms import UpdatePasswordForm
from django.core.exceptions import ValidationError
from .encrypt_util import encrypt, decrypt , generate_random_password
from django.http import HttpResponseRedirect, JsonResponse
@login_required
def home(request):
    return render(request, 'generator/home.html')

# add new password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_new_password(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', request.path))
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = encrypt(request.POST['password'])
            messages.success(request, f"New password added for {username}.")
            UserPassword.objects.create(username=username, password=password,user=request.user)
            return HttpResponseRedirect("/add-password")
        except Exception as error:
            print("Error: ", error)

    return render(request, 'generator/add-password.html')


# edit password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_password(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', request.path))
    user_password = UserPassword.objects.get(id=pk)
    user_password.password = decrypt(user_password.password)
    form = UpdatePasswordForm(instance=user_password)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # delete password
            user_password.delete()
            return redirect('/manage-passwords')
        form = UpdatePasswordForm(request.POST, instance=user_password)

        if form.is_valid():
            try:
                user_password.password = encrypt(user_password.password)
                form.save()
                messages.success(request, "Password updated.")
                user_password.password = decrypt(user_password.password)
                return HttpResponseRedirect(request.path)
            except ValidationError as e:
                form.add_error(None, e)

    context = {'form': form}
    return render(request, 'generator/edit-password.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manage_passwords(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', request.path))
    sort_order = 'asc'
    logged_in_user = request.user
    user_passwords = UserPassword.objects.filter(user=logged_in_user)
    if request.GET.get('sort_order'):
        sort_order = request.GET.get('sort_order', 'desc')
        user_passwords = user_passwords.order_by('-date_created' if sort_order == 'desc' else 'date_created')
    if not user_passwords:
        print("No password error")
        return render(request, 'generator/manage-passwords.html',
                      {'no_password': "No password available. Please add password."})
    return render(request, 'generator/manage-passwords.html', {'all_passwords': user_passwords, 'sort_order': sort_order})


# generate random password
def generate_password(request):
    password = generate_random_password()
    return JsonResponse({'password': password})