from django import forms
from django.forms import ModelForm, DateInput
from scheduler.models import Event, Schedule, Friend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['visibility','start_time','end_time','start_date','end_date',
                'sunday','monday','tuesday','wednesday','thursday','friday','saturday',
                'name','location','description']
        widgets = {
                'start_date': DateInput(attrs={'class':'datepicker'}),
                'end_date': DateInput(attrs={'class':'datepicker'})
                }
class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['visibility','name']

class AddFriendForm(forms.Form):
    newfriend = forms.CharField(max_length=100)

    def clean_newfriend(self):
        if User.objects.filter(username=self.cleaned_data["newfriend"]).exists():
            return self.cleaned_data["newfriend"]
        else:
            raise ValidationError("User does not exist.")

    def get_newfriend_user(self):
        return User.objects.get(username=self.cleaned_data["newfriend"])
