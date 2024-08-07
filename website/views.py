

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .forms import SignUpForm, AddRecordForm, TaskForm, InteractionForm
from .models import Records, Task, Interaction, SalesRep
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Sum


"""def home(request):
	records = Records.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})"""

def home(request):
	query = request.GET.get('q')
	if query:
		records = Records.objects.filter(
			Q(first_name__icontains=query) |
			Q(last_name__icontains=query) |
			Q(email__icontains=query) |
			Q(phone__icontains=query) |
			Q(address__icontains=query) |
			Q(city__icontains=query) |
			Q(state__icontains=query) |
			Q(zipcode__icontains=query)
		)
	else:
		records = Records.objects.all()

	tasks = Task.objects.all()

	# Get the current month
	now = timezone.now()
	current_month_start = now.replace(day=1)
	next_month = (current_month_start + timezone.timedelta(days=32)).replace(day=1)

    # Filter records for the current month
	current_month_records = Records.objects.filter(created_at__gte=current_month_start, created_at__lt=next_month)

    # Aggregate data
	sales_made = current_month_records.count()
	kw_sold = current_month_records.aggregate(Sum('system_size'))['system_size__sum'] or 0
	revenue_generated = current_month_records.aggregate(Sum('estimated_cost'))['estimated_cost__sum'] or 0

	# Calculate top sales representative
	top_sales_rep = current_month_records.values('sales_representative').annotate(
		total_sales=Count('id')
	).order_by('-total_sales').first()

	lead_sources = current_month_records.values('lead_source').annotate(count=Count('id'))
	lead_source_data = {item['lead_source']: item['count'] for item in lead_sources}

	print("Records:", list(records.values()))
	print("Tasks:", list(tasks.values()))
	print("Sales made this month:", sales_made)
	print("kW sold this month:", kw_sold)
	print("Revenue generated this month:", revenue_generated)

	context = {
        'records': records,
		'tasks': tasks,
        'sales_made': sales_made,
        'kw_sold': kw_sold,
        'revenue_generated': revenue_generated,
		'top_sales_rep': top_sales_rep,
    }

    # Check to see if logging in
	"""if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
        # Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', context)"""
	if request.method == 'POST':
		if 'username' in request.POST and 'password' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			# Authenticate
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "You Have Been Logged In!")
				return redirect('home')
			else:
				messages.success(request, "There Was An Error Logging In, Please Try Again...")
				return redirect('home')
		else:
			task_form = TaskForm(request.POST)
			if task_form.is_valid():
				task_form.save()
				messages.success(request, "Task added successfully!")
				return redirect('home')
			else:
				context['task_form'] = task_form
				messages.error(request, "Error adding task.")
    
	return render(request, 'home.html', context)
	


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Records.objects.get(id=pk)
		interactions = customer_record.interactions.all()
		return render(request, 'record.html', {'customer_record':customer_record, 'interactions': interactions})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Records.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None, request.FILES or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			print(request.FILES)
			if form.is_valid():
				add_record = form.save()

				 # Send email after saving the record
				subject = 'Congratulations on your closed deal!'
				message = f"""
				\nCongratulations on your closed deal! Here is the information so you don't forget.

				Details:
				Name: {add_record.first_name} {add_record.last_name}
				Email: {add_record.email}
				Phone: {add_record.phone}
				Address: {add_record.address}, {add_record.city}, {add_record.state} {add_record.zipcode}
				Lead Source: {add_record.lead_source}
				Project Status: {add_record.project_status}
				Installation Date: {add_record.installation_date}
				System Size (kW): {add_record.system_size}
				Estimated Cost: {add_record.estimated_cost}
				Sales Representative: {add_record.sales_representative}
				Notes: {add_record.notes}
				Incentives: {add_record.incentives}
				"""
				from_email = 'letsgonets03@gmail.com'
				recipient_list = ['letsgonets03@gmail.com']
				send_mail(subject, message, from_email, recipient_list)


				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

"""def update_record(request, pk):
	
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                print("Form is valid, saving record...")
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')  # Redirect to the home page after updating the record
            else:
                print("Form is not valid")
                print(form.errors)  # Print form errors
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')"""

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, request.FILES or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                print("Form is valid, saving record...")
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')  # Redirect to the home page after updating the record
            else:
                print("Form is not valid")
                print(form.errors)  # Print form errors
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

	

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Added Successfully")
            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def add_interaction(request, record_id):
    record = get_object_or_404(Records, id=record_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.record = record
            interaction.save()
            messages.success(request, "Interaction has been added.")
            return redirect('record', pk=record_id)
    else:
        form = InteractionForm()
    return render(request, 'add_interaction.html', {'form': form, 'record': record})

def email_customer_info(request, pk):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(Records, id=pk)
        subject = 'Customer Information'
        message = f"""
        Customer Information:
        
        Name: {customer_record.first_name} {customer_record.last_name}
        Email: {customer_record.email}
        Phone: {customer_record.phone}
        Address: {customer_record.address}
        City: {customer_record.city}
        State: {customer_record.state}
        Zipcode: {customer_record.zipcode}
        Lead Source: {customer_record.lead_source}
        Project Status: {customer_record.project_status}
        Installation Date: {customer_record.installation_date}
        System Size (kW): {customer_record.system_size}
        Estimated Cost: {customer_record.estimated_cost}
        Sales Representative: {customer_record.sales_representative}
        Notes: {customer_record.notes}
        Incentives: {customer_record.incentives}
        Date Signed: {customer_record.created_at}
        ID: {customer_record.id}
        """
        if customer_record.contract:
            message += f"Contract: {request.build_absolute_uri(customer_record.contract.url)}"
        else:
            message += "Contract: No contract uploaded"

        from_email = 'letsgonets03@gmail.com'
        recipient_list = ['jimmybradford55@yahoo.com']

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, "Customer information has been emailed successfully!")
        return redirect('record', pk=pk)
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('home')
	
def dashboard(request):
    total_sales = Records.objects.filter(created_at__month=timezone.now().month).count()
    total_kw = Records.objects.filter(created_at__month=timezone.now().month).aggregate(Sum('system_size'))['system_size__sum']
    total_revenue = Records.objects.filter(created_at__month=timezone.now().month).aggregate(Sum('estimated_cost'))['estimated_cost__sum']
    top_reps = Records.objects.values('sales_representative').annotate(total_sales=Count('id')).order_by('-total_sales')[:3]
    
    context = {
        'total_sales': total_sales,
        'total_kw': total_kw,
        'total_revenue': total_revenue,
        'top_reps': top_reps,
    }
    return render(request, 'dashboard.html', context)