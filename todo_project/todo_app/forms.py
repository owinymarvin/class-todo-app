import datetime
from django import forms
from . models import TodoAppModel

class TodoAppForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','min':datetime.datetime.today().date()}))
    due_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = TodoAppModel
        fields = ['title', 'description', 'completed', 'due_date', 'due_time']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class']='form-control'
        self.fields['description'].widget.attrs['class']='form-control'
        self.fields['due_date'].widget.attrs['class']='form-control'
        self.fields['due_time'].widget.attrs['class']='form-control'