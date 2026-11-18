from django import forms

from .models import SchoolRegistrationRequest, SchoolActivity


class SchoolRegistrationForm(forms.ModelForm):

    class Meta:

        model = SchoolRegistrationRequest

        fields = [
            "school_name",
            "district",
            "province",
            "school_type",
            "ownership",
            "contact_person",
            "email",
            "phone",
            "website",
            "message",
        ]

        widgets = {

            "school_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter official school name"
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "placeholder": "District"
                }
            ),

            "province": forms.TextInput(
                attrs={
                    "placeholder": "Province"
                }
            ),

            "school_type": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Secondary, Primary, TVET"
                }
            ),

            "ownership": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Public, Private"
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "placeholder": "Authorized contact person's name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Official school email"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "School phone number"
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Tell us anything important about "
                        "your school or registration request."
                    ),
                    "rows": 5,
                }
            ),
        }
class SchoolActivityForm(forms.ModelForm):

    class Meta:
        model = SchoolActivity

        fields = [
            "title",
            "description",
            "image",
            "activity_date",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Event or news title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write the event or news description...",
                    "rows": 7,
                }
            ),

            "activity_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }        