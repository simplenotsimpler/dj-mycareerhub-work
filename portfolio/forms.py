import time
from django import forms
from .models import ContactSubmission

from portfolio.models import NavItem


class NavItemAdminForm(forms.ModelForm):
    # used in admin.py/NavItemAdmin
    class Meta:
        model = NavItem
        fields = '__all__'
        widgets = {
            'order': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
        }


class ContactSubmissionForm(forms.ModelForm):
    # Honeypot field – not part of the model
    # Use a text input hidden with CSS instead of HiddenInput,
    # because bots often skip type="hidden" fields. Real users won’t see it.
    nickname = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',       # skipped in tab order
            'aria-hidden': 'true',  # hidden from assistive tech
            'class': 'honeypot-field',
        })
    )

    # Timestamp field for time-based check
    start_time = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'contact-form-input',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'contact-form-input',
                'id': 'contact-email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'contact-form-input',
                'id': 'contact-phone',
            }),
            'message': forms.Textarea(attrs={
                'class': 'contact-form-textarea',
                'id': 'contact-message',
            }),
        }

    def clean_nickname(self):
        """Check if the honeypot field was filled — if yes, it's likely a bot."""
        value = self.cleaned_data.get('nickname')
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    # Time-based check validation
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time:
            elapsed = time.time() - start_time
            # print(f"[DEBUG] Elapsed time: {elapsed:.2f} seconds")
            if elapsed < 3:  # less than 3 seconds is suspicious
                raise forms.ValidationError(
                    "Form submitted too quickly. Spam suspected.")
        return start_time
