from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import user_type_required, redirect_authenticated_user


from apps.user.forms import *
from apps.user.models import CustomUser, TYPE_CHOICES
from apps.route.models import RouteWeekday, Route, RouteDiscount

@login_required
def index(request):
    users = CustomUser.objects.filter(is_superuser= False).order_by('full_name')
    all_types = TYPE_CHOICES
    all_status = ('Ativo', 'Inativo')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password') if request.POST.__contains__('password') else None
        type = request.POST.get('type')
        status = request.POST.get('status')
        issuance_type = request.POST.get('issuance_type')

        if status == 'Ativo':
            status = True
        elif status == 'Inativo':
            status = False
        else:
            status = None

        user = CustomUser.objects.get(id=user_id)
        user.full_name = name
        user.phone = phone
        user.type = type
        user.is_active = status

        user.upload_ticket = type == 'F' and issuance_type == 'bilhete' 

        if password:
            user.set_password(password)
        user.save()

        return redirect(reverse('user:index'))
    
    return render(request, 'user/index.html', {
        'users': users, 
        'all_types': all_types, 
        'all_status': all_status,
    })

@redirect_authenticated_user
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            return redirect(reverse('user:login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/auth.html', {'form': form, 'auth': 'signup'})


@redirect_authenticated_user
def user_login(request):
    form = UserAuthenticationForm()

    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)

        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if phone:
            username = phone

        # Use authenticate para verificar as credenciais
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Use login para autenticar o usuário na sessão
            login(request, user)

            return redirect(reverse('core:index'))
        else:
            # Adicione uma mensagem de erro para indicar credenciais inválidas
            form.add_error(None, 'Credenciais inválidas. Por favor, tente novamente.')

    return render(request, 'user/auth.html', {'form': form, 'auth': 'login'})


@login_required
def user_edit(request):
    user = request.user
    form = CustomUserChangeForm(instance=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=user)
        if form.is_valid():
            if not form.cleaned_data['password']:
                del form.cleaned_data['password']
            
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
                user.save()
            else:
                form.save()

            return redirect(reverse('core:index'))
    return render(request, 'user/auth.html', {'form': form, 'auth': 'edit'})


def user_logout(request):
    logout(request)
    return redirect(reverse('user:login'))

@login_required
def view(request, id):
    user = CustomUser.objects.get(id= id)

    user_types = TYPE_CHOICES
    user_status = ('Ativo', 'Inativo')

    routes_ids = RouteWeekday.objects.filter(boat__supplier= user).values_list('route', flat= True).distinct()

    user_routes = Route.objects.filter(id__in= routes_ids)

    user_route_discounts = RouteDiscount.objects.filter(supplier= user)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password') if request.POST.__contains__('password') else None
        type = request.POST.get('type')
        status = request.POST.get('status')
        issuance_type = request.POST.get('issuance_type')

        if status == 'Ativo':
            status = True
        elif status == 'Inativo':
            status = False
        else:
            status = None

        user.full_name = name
        user.phone = phone
        user.type = type
        user.is_active = status

        user.upload_ticket = type == 'F' and issuance_type == 'bilhete' 

        if password:
            user.set_password(password)
        user.save()

        for item in request.POST.items():
            if 'new_discounted_value' in item[0]:
                route_id = item[0].split('_')[4]
                route = Route.objects.get(id = route_id)

                new_discouted_cost = request.POST[f'new_discounted_cost_route_{ route_id }']

                active = request.POST.__contains__(f'discount-{ route_id }')

                RouteDiscount.objects.create(
                    supplier = user,
                    route = route,
                    discounted_value = item[1],
                    discounted_cost = new_discouted_cost,
                    is_active= active
                )

            if 'discounted_value' in item[0] and not 'new' in item[0]:
                route_discount_id = item[0].split('_')[2]
                route_id = item[0].split('_')[4]

                dicounted_cost = request.POST[f'discounted_cost_{ route_discount_id }_route_{ route_id }']

                active = request.POST.__contains__(f'discount-{ route_id }')


                route_discount = RouteDiscount.objects.get(id= route_discount_id)
                
                route_discount.discounted_value = item[1].replace(',', '.')
                route_discount.discounted_cost = dicounted_cost.replace(',', '.')
                route_discount.is_active = active
                route_discount.save()
                
        messages.success(request, 'Dados alterados com sucesso!')

    return render(request, 'user/view.html', {
        'user': user,
        'user_routes': user_routes,
        'user_status': user_status,
        'user_route_discounts': user_route_discounts,
        'user_types': user_types,
    })