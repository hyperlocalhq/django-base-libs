# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from decimal import Decimal

from django import forms
from django.utils.timezone import now as tz_now

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

def current_time():
    return tz_now().time()

class DummyForm(forms.Form):
    title = forms.CharField(label="Title", help_text="How should we name it?")
    description = forms.CharField(label="Description", widget=forms.Textarea(), help_text="Enter a short description. Maximal 30 words.")
    content = forms.CharField(label="Content", widget=forms.Textarea())
    published = forms.BooleanField(label="Published", required=False)
    featured = forms.BooleanField(label="Featured", required=False, help_text="Featured items will appear on the start page.")
    color = forms.ChoiceField(label="Color you like", choices=(("red", "Red"),("green", "Green"),("blue", "Blue")), help_text="What is your favorite color?")
    color2 = forms.ChoiceField(label="Color you don't like", widget=forms.RadioSelect(), choices=(("red", "Red"),("green", "Green"),("blue", "Blue")), help_text="What is your least favorite color?")
    stars = forms.TypedChoiceField(label="Stars", choices=((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five")), help_text="How would you rate it?")
    start = forms.DateField(label="Start", initial=date.today, help_text="When will it start?")
    vernissage = forms.DateTimeField(label="Vernissage", initial=tz_now, help_text="When should we gather for a vernissage?")
    now = forms.TimeField(label="Time now", initial=current_time, help_text="What time is it now?")
    price = forms.DecimalField(label="Price", max_digits=5, decimal_places=2, initial=Decimal("2.50"), help_text="Admission price for this event.")
    email = forms.EmailField(label="Email", initial="demo@example.com", help_text="Your email address")
    document = forms.FileField(label="Document", help_text="Choose a document to upload.")
    latitude = forms.FloatField(label="Latitude", initial=52.51883,  help_text="What is the latitude of you geoposition?")
    image = forms.ImageField(label="Image", help_text="Choose an image to upload.")
    number = forms.IntegerField(label="Favorite number", initial=7, help_text="What is your favorite number?")
    ip_address = forms.IPAddressField(label="IP Address", initial="127.0.0.1", help_text="IP address of your computer.")
    spoken_languages = forms.MultipleChoiceField(label="Spoken languages", choices=(("en", "English"), ("de", "German"), ("fr", "French")), help_text="Choose languages you can speak.")
    written_languages = forms.MultipleChoiceField(label="Written languages", widget=forms.CheckboxSelectMultiple, choices=(("en", "English"), ("de", "German"), ("fr", "French")), help_text="Choose languages you can read and write.")
    website = forms.URLField(label="Website", initial="http://example.com", help_text="Website URL.")
    
    def __init__(self, *args, **kwargs):
        super(DummyForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = [layout.Fieldset(
            "Main data",
            "title",
            "description",
            "content",
            "published",
            "featured",
        ), layout.Fieldset(
            "Categories",
            "color",
            "color2",
            "stars",
            "spoken_languages",
            "written_languages",
        ), layout.Fieldset(
            "Date and time",
            "start",
            "opening",
            "now",
        ), layout.Fieldset(
            "Files",
            "document",
            "image",
        ), layout.Fieldset(
            "The rest",
            "email",
            "website",
            "price",
            "latitude",
            "number",
            "ip_address",
        ), bootstrap.FormActions(
            layout.Submit('reset', 'Reset', css_class="btn-warning"),
            layout.Submit('submit', 'Submit'),
        )]

        self.helper.layout = layout.Layout(
            *layout_blocks
            )        
    
    
    
