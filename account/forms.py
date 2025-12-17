from django import forms
from django.contrib.auth.hashers import make_password

from .models import CustomUser


# Base form with automatic bootstrap styling
class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)

        # Apply Bootstrap and custom colors
        for field in self.visible_fields():
            field.field.widget.attrs.update({
                'class': 'form-control shadow-sm border-0 rounded-3',
                'style': 'background:#f8f9fa; padding:10px;'
            })


class CustomUserForm(FormSettings):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email',
            'class': 'form-control shadow-sm border-primary rounded-3',
            'style': 'background:#e7f1ff; padding:10px;'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control shadow-sm border-danger rounded-3',
            'style': 'background:#ffecec; padding:10px;'
        })
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):  # Edit mode
            instance = kwargs.get('instance').__dict__

            self.fields['password'].required = False

            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)

            if self.instance.pk is not None:
                self.fields['password'].widget.attrs.update({
                    'placeholder': "Fill only if you want to change password",
                    'style': 'background:#fff3cd; padding:10px;'  # Yellow for warning
                })

        else:  # Create mode
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

            # Make first/last name fields visually appealing
            self.fields['first_name'].widget.attrs.update({
                'class': 'form-control shadow-sm rounded-3 border-success',
                'style': 'background:#eaffea; padding:10px;'
            })
            self.fields['last_name'].widget.attrs.update({
                'class': 'form-control shadow-sm rounded-3 border-success',
                'style': 'background:#eaffea; padding:10px;'
            })

    def clean_email(self):
        form_email = self.cleaned_data['email'].lower()

        if self.instance.pk is None:  # New user
            if CustomUser.objects.filter(email=form_email).exists():
                raise forms.ValidationError("The given email is already registered")
        else:  # Update
            db_email = self.Meta.model.objects.get(id=self.instance.pk).email.lower()
            if db_email != form_email:
                if CustomUser.objects.filter(email=form_email).exists():
                    raise forms.ValidationError("The given email is already registered")

        return form_email

    def clean_password(self):
        password = self.cleaned_data.get("password", None)

        if self.instance.pk is not None:  # Updating user
            if not password:
                return self.instance.password  # Keep old password

        return make_password(password)

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'email', 'password']



