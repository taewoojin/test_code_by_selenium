from django import forms
from django.core.exceptions import ValidationError
from .models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "이미 리스트에 해당 아이템이 있습니다"


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
        
    def save(self, for_list):
        self.instance.list = for_list
        return super(ItemForm, self).save()


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super(ExistingListItemForm, self).__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.ModelForm.save(self)