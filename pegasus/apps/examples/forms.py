from django import forms


class ExampleForm(forms.Form):
    COLORS = (
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
    )
    name = forms.CharField(help_text='This is a character field. It is required.')
    email = forms.EmailField(help_text='This is an email field. It is required.')
    invisible = forms.CharField(help_text='This is an Invisible field.', widget=forms.HiddenInput(),
                                initial='something')
    website = forms.URLField(help_text='This is a URL field. It is required.')
    checkbox = forms.BooleanField(help_text='This is a checkbox / boolean field', required=False)
    favorite_color = forms.ChoiceField(help_text='This is a choice field', choices=COLORS)
    comments = forms.CharField(help_text='This is a longer character field. It is optional', required=False,
                               widget=forms.Textarea())
