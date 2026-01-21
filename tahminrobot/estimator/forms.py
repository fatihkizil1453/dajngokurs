from django import forms


class EstimateForm(forms.Form):
    square_meters = forms.FloatField(
        label='Square meters', min_value=1, max_value=10000,
        widget=forms.NumberInput(attrs={'placeholder': 'örn. 90', 'class': 'form-control form-control-lg'})
    )
    rooms = forms.IntegerField(
        label='Number of rooms', min_value=1, max_value=20,
        widget=forms.NumberInput(attrs={'placeholder': 'örn. 3', 'class': 'form-control form-control-lg'})
    )
    floor = forms.IntegerField(
        label='Floor', min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'placeholder': 'örn. 2', 'class': 'form-control form-control-lg'})
    )
    age = forms.IntegerField(
        label='Age of building (years)', min_value=0, max_value=500,
        widget=forms.NumberInput(attrs={'placeholder': 'örn. 10', 'class': 'form-control form-control-lg'})
    )

    location_rating = forms.IntegerField(
        label='Location rating (1-10)', min_value=1, max_value=10, initial=5,
        widget=forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'min': '1', 'max': '10'})
    )

    TRANSPORT_CHOICES = [
        ('kolay', 'Kolay'),
        ('orta', 'Orta'),
        ('zor', 'Zor'),
    ]
    transport = forms.ChoiceField(label='Ulaşım durumu', choices=TRANSPORT_CHOICES, initial='orta',
                                  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    def clean(self):
        cleaned = super().clean()
        sqm = cleaned.get('square_meters')
        rooms = cleaned.get('rooms')
        floor = cleaned.get('floor')
        age = cleaned.get('age')

        # Extra sanity checks
        if sqm and rooms and (sqm / rooms) < 9:
            raise forms.ValidationError('Metrekare başına oda oranı çok düşük görünüyor — lütfen değerleri kontrol edin.')

        if age and age > 200:
            raise forms.ValidationError('Bina yaşı çok büyük görünüyor — lütfen tekrar kontrol edin.')

        return cleaned
