from django.forms import ModelForm
from scheduler.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['visibility','start_time','end_time','start_date','end_date',
                'sunday','monday','tuesday','wednesday','thursday','friday','saturday',
                'name','location','description']
