from django import forms
from CVapp.models import Interaction, FollowBack, Parameters

class jobCreateForm(forms.ModelForm):
    class Meta:
        model = Interaction
        exclude = ('userName','interactionDateTime',)


