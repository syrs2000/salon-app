from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # お客様に入力してもらう項目だけを指定
        fields = ['name']
        
        # 画面上のラベルや見た目の調整
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 山田 花子'}),
           
        }