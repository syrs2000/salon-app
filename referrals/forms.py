from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fieldsに phone_number を追加
        fields = ['name', 'phone_number']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: はなちゃん'}),
            # 電話番号の入力欄設定
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 090-1234-5678（任意）'}),
        }