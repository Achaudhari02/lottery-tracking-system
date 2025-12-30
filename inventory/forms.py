from django.forms import ModelForm
from .models import Pack


class PackForm(ModelForm):
    class Meta:
        model = Pack
        fields = '__all__'

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barcode'].widget.attrs.update({'class':'block min-w-0 grow bg-gray-200 outline-solid py-1.5 pr-3 pl-1 text-base text-white placeholder:text-gray-500 focus:outline-solid sm:text-sm/6', 'placeholder': 'Barcode'})