from django import forms


class ReviewForm(forms.Form):
    valoration = forms.IntegerField(
        widget=forms.RadioSelect(
            choices=[
                (5, 'Muy bueno'), (4, 'Bueno'),
                (3, 'Normal'), (2, 'Malo'), (1, 'Muy Malo')
            ]
        ),
        label='Valoracion'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 50}), label=''
    )
