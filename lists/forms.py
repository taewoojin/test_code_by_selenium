from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        # widget 커스터마이징
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': '작업 아이템 입력',
                'class': 'form-control input-lg',
            })
        }
        # 에러메시지 커스터마이징
        error_messages = {
            'text': {'required': "You can't have an empty list item"}
        }