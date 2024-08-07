from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Records, Interaction

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "City", "class": "form-control"}), label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "State", "class": "form-control"}), label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}), label="")
    lead_source = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Lead Source", "class": "form-control"}), label="")
    project_status = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Project Status", "class": "form-control"}), label="")
    installation_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Installation Date"
    )
    system_size = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "System Size (kW)", "class": "form-control"}), label="")
    estimated_cost = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Estimated Cost", "class": "form-control"}), label="")
    sales_representative = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Sales Representative", "class": "form-control"}), label="")
    notes = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Notes", "class": "form-control"}), label="")
    incentives = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder": "Incentives", "class": "form-control"}), label="")
    contract = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"}), label="")
    

    class Meta:
        model = Records
        fields = '__all__'

# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'date', 'notes', 'outcome']
        widgets = {
            'interaction_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'outcome': forms.TextInput(attrs={'class': 'form-control'}),
        }


            

            
    