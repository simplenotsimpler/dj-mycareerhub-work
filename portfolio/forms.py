from django import forms

from portfolio.models import NavItem


class NavItemAdminForm(forms.ModelForm):
    class Meta:
        model = NavItem
        fields = '__all__'
        widgets = {
            'order': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
        }