from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='', required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder' : 'Usuario', 'class' : 'form-control'}))
    password = forms.CharField(label='', required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder' : 'Contraseña', 'class' : 'form-control', 'type' : 'password', 'id' : 'pass'}))

class NewUserForm(forms.Form):
    firstname = forms.CharField(label='Nombre', required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder' : 'Nombre', 'class' : 'form-control'}))
    lastname = forms.CharField(label='Apellido', required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder' : 'Apellido', 'class' : 'form-control'}))
    dni = forms.IntegerField(label='DNI', required=True, widget=forms.NumberInput(attrs={'placeholder' : 'DNI', 'class' : 'form-control'}))
    dob = forms.CharField(label='Fecha de nacimiento', required=True, widget=forms.TextInput(attrs={'placeholder' : 'Fecha de nacimiento', 'class' : 'form-control marginer', 'id' : 'datePicker'}))
    email = forms.EmailField(label='Email', required=True, max_length=100, widget=forms.EmailInput(attrs={'placeholder' : 'Email', 'class' : 'form-control'}))
    username = forms.CharField(label='Usuario', required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder' : 'Usuario', 'class' : 'form-control'}))
    password = forms.CharField(label='Contraseña', required=True, max_length=100, widget=forms.PasswordInput(attrs={'placeholder' : 'Contraseña', 'class' : 'form-control', 'type' : 'password', 'id' : 'pass'}))