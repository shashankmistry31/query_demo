from django  import forms

class BinForm(forms.Form):
    # binary_data = forms.CharField(label='Query', max_length=200)
    query = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))

class DecForm(forms.Form):
    decimal_data = forms.CharField(label='Integer Value', max_length=16)
