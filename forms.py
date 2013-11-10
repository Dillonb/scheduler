from django.forms import ModelForm, DateInput
from scheduler.models import Event, Schedule

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
        
