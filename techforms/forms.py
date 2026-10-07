from django import forms
from .models import TRLAssessment, InnovationVoucherApplication, PatentApplication, PriorArtSearch, TrademarkApplication, ExpressInterest
import logging
from datetime import date
import re
import json
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import State, District
from django.utils import timezone
from django import forms
from .models import TrademarkApplication, Patent
from tech_repo.models import Inventor, State, District
import re
import logging
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger(__name__)



class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ['applicant_name', 'email', 'contact_number', 'address', 'country', 'state', 'district', 'title', 'description', 'pdf_write', 'word_write', 'sector']
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control zoom-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'address': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'country': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'state': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'district': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'pdf_write': forms.FileInput(attrs={'class': 'form-control'}),
            'word_write': forms.FileInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-select zoom-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        required_fields = ['applicant_name', 'email', 'contact_number', 'address', 'country', 'state', 'district', 'title', 'description', 'sector']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")

        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")

        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")

        return cleaned_data




class ExpressInterestForm(forms.ModelForm):
    other_interest = forms.CharField(max_length=255, required=False)

    class Meta:
        model = ExpressInterest
        fields = ['applicant_name', 'email', 'contact_number', 'organization_name', 'role',
                  'patent_title', 'area_of_interest', 'location',
                  'reason', 'notes', 'agree_to_contact']
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control zoom-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'role': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'patent_title': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'area_of_interest': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'location': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'agree_to_contact': forms.CheckboxInput(attrs={'style': 'width: fit-content;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Express Interest form data: {cleaned_data}")
        
        required_fields = ['applicant_name', 'email', 'contact_number', 'organization_name', 'role',
                      'patent_title', 'area_of_interest', 'location', 'agree_to_contact']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")

        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")

        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")

        agree_to_contact = cleaned_data.get('agree_to_contact')
        if not agree_to_contact:
            self.add_error('agree_to_contact', "You must agree to be contacted.")

        # Validate other_interest if area_of_interest is 'other' (though it should be updated by now)
        area_of_interest = cleaned_data.get('area_of_interest')
        other_interest = cleaned_data.get('other_interest')
        if area_of_interest == 'other' and not other_interest:
            self.add_error('other_interest', "Please specify the other area of interest.")
        elif other_interest and area_of_interest != other_interest:
            cleaned_data['area_of_interest'] = other_interest

        return cleaned_data

class TRLAssessmentForm(forms.ModelForm):
    class Meta:
        model = TRLAssessment
        fields = ['inventor_name', 'organisation', 'email', 'contact_number', 'technology_title',
                  'field_of_invention', 'technology_description', 'market_segment', 'patent_details']
        widgets = {
            'technology_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'inventor_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'organisation': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control zoom-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'technology_title': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'field_of_invention': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'market_segment': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'patent_details': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning TRL Assessment form data: {cleaned_data}")

        required_fields = ['inventor_name', 'organisation', 'email', 'contact_number', 'technology_title',
                           'field_of_invention', 'technology_description', 'market_segment', 'patent_details']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")

        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")

        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")

        return cleaned_data




class TrademarkApplicationFormStep1(forms.ModelForm):
    class Meta:
        model = TrademarkApplication
        fields = ['startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 'email', 
                  'contact_number', 'company_classification', 'date_of_registration', 'uam_certificate', 
                  'website', 'inventor_count']
        widgets = {
            'date_of_registration': forms.DateInput(attrs={'type': 'date'}),
            'uam_certificate': forms.ClearableFileInput(),
            'state': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'district': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'website': forms.URLInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].required = False

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Step 1 form data: {cleaned_data}")

        # Validate required Step 1 fields (excluding website)
        step1_fields = ['startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 
                        'email', 'contact_number', 'company_classification', 'inventor_count']
        for field in step1_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        # Validate uam_certificate
        if not cleaned_data.get('uam_certificate'):
            self.add_error('uam_certificate', "UAM certificate is required.")
            logger.error("Validation error: uam_certificate is missing")

        # Validate date_of_registration
        date_of_registration = cleaned_data.get('date_of_registration')
        if date_of_registration:
            if date_of_registration > timezone.now().date():
                self.add_error('date_of_registration', "Date of registration cannot be in the future.")
                logger.error("Validation error: date_of_registration is in the future")
        else:
            self.add_error('date_of_registration', "Date of registration is required.")
            logger.error("Validation error: date_of_registration is missing")

        # Validate email format
        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")
            logger.error("Validation error: invalid email format")

        # Validate website URL if provided
        website = cleaned_data.get('website')
        if website and not re.match(r'^(https?:\/\/)?([\w\-]+\.)*[\w\-]+(\.[\w\-]+)+([\/\w\.\-\?=&%]*)?$', website):
            self.add_error('website', "Please enter a valid URL (e.g., https://example.com or https://example.com/path).")
            logger.error("Validation error: invalid website URL")

        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")
            logger.error("Validation error: invalid contact number")

        inventor_count = cleaned_data.get('inventor_count')
        if inventor_count is None or inventor_count < 0:
            self.add_error('inventor_count', "Please enter a valid number of inventors (minimum 0).")
            logger.error("Validation error: invalid or missing inventor_count")
        else:
            inventor_count = int(inventor_count)

        # Store inventor details in cleaned_data for later use
        cleaned_data['inventors'] = []
        for i in range(1, inventor_count + 1):
            name = self.data.get(f'inventorName{i}')
            designation = self.data.get(f'inventorDesignation{i}')
            dob = self.data.get(f'inventorDOB{i}')
            aadhaar = self.files.get(f'inventorAadhaar{i}')
            mobile = self.data.get(f'inventorMobile{i}')
            email = self.data.get(f'inventorEmail{i}')

            if not all([name, designation, dob, aadhaar, mobile, email]):
                self.add_error(None, f"All details for Inventor {i} are required.")
                logger.error(f"Validation error: Inventor {i} details incomplete")
            elif not re.match(r'^\d{10}$', mobile):
                self.add_error(None, f"Invalid mobile number for Inventor {i}. Must be exactly 10 digits.")
                logger.error(f"Validation error: invalid mobile number for Inventor {i}")
            elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                self.add_error(None, f"Invalid email address for Inventor {i}.")
                logger.error(f"Validation error: invalid email for Inventor {i}")
            elif aadhaar and not aadhaar.name.endswith('.pdf'):
                self.add_error(None, f"Invalid file format for Inventor {i} Aadhaar. Must be a PDF.")
                logger.error(f"Validation error: invalid Aadhaar file format for Inventor {i}")
            else:
                cleaned_data['inventors'].append({
                    'name': name.strip(),
                    'designation': designation.strip(),
                    'dob': dob,
                    'aadhaar': aadhaar,
                    'mobile': mobile.strip(),
                    'email': email.strip()
                })

        return cleaned_data


class TrademarkApplicationFormStep2(forms.ModelForm):
    class Meta:
        model = TrademarkApplication
        fields = ['slogan', 'color_combination', 'three_dimensional_mark', 'class_details', 'trademark_image', 
                  'trademark_status', 'proof_of_use', 'duration_of_use', 'supporting_proof']
        widgets = {
            'slogan': forms.Textarea(attrs={'rows': 3}),
            'color_combination': forms.Textarea(attrs={'rows': 3}),
            'three_dimensional_mark': forms.Textarea(attrs={'rows': 3}),
            'class_details': forms.Textarea(attrs={'rows': 3}),
            'trademark_image': forms.ClearableFileInput(),
            'trademark_status': forms.Textarea(attrs={'rows': 3}),
            'proof_of_use': forms.ClearableFileInput(attrs={'required': 'required'}),
            'duration_of_use': forms.Textarea(attrs={'rows': 3}),
            'supporting_proof': forms.ClearableFileInput(attrs={'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Step 2 form data: {cleaned_data}")

        step2_fields = ['slogan', 'color_combination', 'three_dimensional_mark', 'class_details', 'trademark_image', 
                       'trademark_status', 'proof_of_use', 'duration_of_use', 'supporting_proof']
        for field in step2_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        trademark_image = cleaned_data.get('trademark_image')
        if trademark_image and not trademark_image.name.endswith(('.ppt', '.pptx', '.pdf')):
            self.add_error('trademark_image', "Please upload a valid file (.ppt, .pptx, or .pdf).")
            logger.error("Validation error: invalid trademark_image file type")

        proof_of_use = cleaned_data.get('proof_of_use')
        if not proof_of_use:
            self.add_error('proof_of_use', "Proof of use is required.")
            logger.error("Validation error: proof_of_use is missing")
        elif not proof_of_use.name.endswith(('.ppt', '.pptx', '.pdf')):
            self.add_error('proof_of_use', "Please upload a valid file (.ppt, .pptx, or .pdf).")
            logger.error("Validation error: invalid proof_of_use file type")

        supporting_proof = cleaned_data.get('supporting_proof')
        if not supporting_proof:
            self.add_error('supporting_proof', "Supporting proof is required.")
            logger.error("Validation error: supporting_proof is missing")
        elif not supporting_proof.name.endswith(('.ppt', '.pptx', '.pdf')):
            self.add_error('supporting_proof', "Please upload a valid file (.ppt, .pptx, or .pdf).")
            logger.error("Validation error: invalid supporting_proof file type")

        return cleaned_data
        
        
class InnovationVoucherFormStep1(forms.ModelForm):
    director_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control zoom-input', 'min': '1', 'max': '10'})
    )

    class Meta:
        model = InnovationVoucherApplication
        fields = [
            'startup_name', 'dpiit_number', 'address', 'country', 'state', 'district',
            'email', 'contact_number', 'company_classification', 'date_of_registration',
            'uam_certificate', 'turnover', 'website', 'director_count'
        ]
        widgets = {
            'startup_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'dpiit_number': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'address': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'country': forms.Select(attrs={'class': 'form-select zoom-input'}, choices=[
                ('', 'Select Country'), ('india', 'India'), ('usa', 'USA'), ('uk', 'UK')
            ]),
            'state': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'district': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control zoom-input', 'pattern': '[0-9]{10}', 'maxlength': '10', 'onkeypress': 'return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))'}),
            'company_classification': forms.Select(attrs={'class': 'form-select zoom-input'}, choices=[
                ('', 'Select company type'),
                ('Micro Enterprise', 'Micro Enterprise'),
                ('Small Enterprise', 'Small Enterprise'),
                ('Medium Enterprise', 'Medium Enterprise'),
                ('Startup', 'Startup (DPIIT Certificated)')
            ]),
            'date_of_registration': forms.DateInput(attrs={'class': 'form-control zoom-input', 'type': 'date', 'max': date.today().isoformat()}),
            'uam_certificate': forms.FileInput(attrs={'class': 'form-control zoom-input', 'accept': '.pdf,.jpg,.png'}),
            'turnover': forms.NumberInput(attrs={'class': 'form-control zoom-input'}),
            'website': forms.URLInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].required = False
        if 'state' in self.data:
            state_id = self.data.get('state')
            self.fields['district'].queryset = District.objects.filter(state_id=state_id) if state_id else District.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Step 1 form data: {cleaned_data}")

        # Validate required fields
        step1_fields = [
            'startup_name', 'dpiit_number', 'address', 'country', 'state', 'district',
            'email', 'contact_number', 'company_classification', 'date_of_registration',
            'uam_certificate', 'director_count'
        ]
        for field in step1_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        # Validate date_of_registration
        date_of_registration = cleaned_data.get('date_of_registration')
        if date_of_registration and date_of_registration > date.today():
            self.add_error('date_of_registration', "Date of registration cannot be in the future.")
            logger.error("Validation error: date_of_registration is in the future")

        # Validate email format
        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")
            logger.error("Validation error: invalid email format")

        # Validate contact_number
        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")
            logger.error("Validation error: invalid contact number")

        # Validate website URL if provided
        website = cleaned_data.get('website')
        if website and not re.match(r'^(https?:\/\/)?([\w\-]+\.)*[\w\-]+(\.[\w\-]+)+([\/\w\.\-\?=&%]*)?$', website):
            self.add_error('website', "Please enter a valid URL (e.g., https://example.com or https://example.com/path).")
            logger.error("Validation error: invalid website URL")

        # Validate director_count
        director_count = cleaned_data.get('director_count')
        if director_count is None or director_count < 1 or director_count > 10:
            self.add_error('director_count', "Please enter a valid number of directors (1-10).")
            logger.error("Validation error: invalid director_count")

        # Validate director details
        cleaned_data['directors'] = []
        if director_count:
            for i in range(1, director_count + 1):
                name = self.data.get(f'director_name_{i}')
                designation = self.data.get(f'director_designation_{i}')
                dob = self.data.get(f'director_dob_{i}')
                aadhar = self.files.get(f'director_aadhar_{i}')
                mobile = self.data.get(f'director_mobile_{i}')
                email = self.data.get(f'director_email_{i}')

                if not all([name, designation, dob, aadhar, mobile, email]):
                    self.add_error(None, f"All details for Director {i} are required.")
                    logger.error(f"Validation error: Director {i} details incomplete")
                elif not re.match(r'^\d{10}$', mobile or ''):
                    self.add_error(None, f"Invalid mobile number for Director {i}. Must be exactly 10 digits.")
                    logger.error(f"Validation error: invalid mobile number for Director {i}")
                elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email or ''):
                    self.add_error(None, f"Invalid email address for Director {i}.")
                    logger.error(f"Validation error: invalid email for Director {i}")
                elif aadhar and not aadhar.name.endswith('.pdf'):
                    self.add_error(None, f"Invalid file format for Director {i} Aadhar. Must be a PDF.")
                    logger.error(f"Validation error: invalid Aadhar file format for Director {i}")
                elif dob and date.fromisoformat(dob) > date.today():
                    self.add_error(None, f"Date of birth for Director {i} cannot be in the future.")
                    logger.error(f"Validation error: invalid DOB for Director {i}")
                else:
                    cleaned_data['directors'].append({
                        'name': name.strip(),
                        'designation': designation.strip(),
                        'dob': dob,
                        'aadhar': aadhar,
                        'mobile': mobile.strip(),
                        'email': email.strip()
                    })

        return cleaned_data

class InnovationVoucherFormStep2(forms.Form):
    voucher_type = forms.ChoiceField(choices=[
        ('A', 'Voucher A – Grant upto Rs.5 lakhs or 80% of Project Cost (for converting the idea into working prototype)'),
        ('B', 'Voucher B – Grant upto Rs.7.5 lakhs or 80% of Project Cost (for converting the prototype into a product)')
    ], required=True, widget=forms.Select(attrs={'class': 'form-select zoom-input'}))
    project_title = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'Enter your project title'}))
    product_name = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'Enter product name'}))
    problem_statement = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe the problem'}))
    solution_proposed = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe the solution'}))
    detailed_description = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Enter detailed description'}))
    invention_upgrade = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Specify invention or upgrade'}))
    scope = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe the scope'}))
    need = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Explain the need'}))
    competitive_advantage = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe the competitive and technical advantage'}))
    social_impact = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe social and environmental impact'}))
    collaboration = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Describe collaborations'}))
    benefits = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Explain expected benefits'}))
    price_advantage = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Explain price advantage'}))
    project_cost = forms.CharField(max_length=5000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Enter total project cost'}))
    target_dates = forms.CharField(max_length=10000, required=True, widget=forms.Textarea(attrs={'class': 'form-control zoom-input', 'rows': '4', 'placeholder': 'Enter target dates'}))
    ppt_upload = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control zoom-input', 'accept': '.ppt,.pptx,.pdf'}))
    youtube_link = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'https://www.youtube.com/watch?v=example'}))

class InnovationVoucherFormStep3(forms.Form):
    outsourcing_charges = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    outsourcing_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    outsourcing_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    raw_materials = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    raw_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    raw_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    fabrication_charges = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    fabrication_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    fabrication_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    ipr_patent = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    ipr_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    ipr_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    testing_validation = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    testing_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    testing_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    commercialization_support = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    commercialization_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    commercialization_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    other1_activity = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width:250px;'}))
    other1_cost = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    other1_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    other1_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    other2_activity = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width:250px;'}))
    other2_cost = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'estimated', 'min': '0', 'step': '0.01'}))
    other2_ivp = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'ivp', 'min': '0', 'step': '0.01'}))
    other2_applicant = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control cost-input', 'data-type': 'applicant', 'min': '0', 'step': '0.01'}))
    total_estimated_cost = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control bg-white', 'readonly': 'readonly'}))
    total_ivp_contribution = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control bg-white', 'readonly': 'readonly'}))
    total_applicant_contribution = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control bg-white', 'readonly': 'readonly'}))

    def clean(self):
        cleaned_data = super().clean()
        total_estimated = (
            cleaned_data.get('outsourcing_charges', 0) +
            cleaned_data.get('raw_materials', 0) +
            cleaned_data.get('fabrication_charges', 0) +
            cleaned_data.get('ipr_patent', 0) +
            cleaned_data.get('testing_validation', 0) +
            cleaned_data.get('commercialization_support', 0) +
            cleaned_data.get('other1_cost', 0) +
            cleaned_data.get('other2_cost', 0)
        )
        total_ivp = (
            cleaned_data.get('outsourcing_ivp', 0) +
            cleaned_data.get('raw_ivp', 0) +
            cleaned_data.get('fabrication_ivp', 0) +
            cleaned_data.get('ipr_ivp', 0) +
            cleaned_data.get('testing_ivp', 0) +
            cleaned_data.get('commercialization_ivp', 0) +
            cleaned_data.get('other1_ivp', 0) +
            cleaned_data.get('other2_ivp', 0)
        )
        total_applicant = (
            cleaned_data.get('outsourcing_applicant', 0) +
            cleaned_data.get('raw_applicant', 0) +
            cleaned_data.get('fabrication_applicant', 0) +
            cleaned_data.get('ipr_applicant', 0) +
            cleaned_data.get('testing_applicant', 0) +
            cleaned_data.get('commercialization_applicant', 0) +
            cleaned_data.get('other1_applicant', 0) +
            cleaned_data.get('other2_applicant', 0)
        )

        if abs(total_estimated - cleaned_data.get('total_estimated_cost', 0)) > 0.01:
            raise forms.ValidationError({'total_estimated_cost': ['Total estimated cost does not match calculated total.']})
        if abs(total_ivp - cleaned_data.get('total_ivp_contribution', 0)) > 0.01:
            raise forms.ValidationError({'total_ivp_contribution': ['Total IVP contribution does not match calculated total.']})
        if abs(total_applicant - cleaned_data.get('total_applicant_contribution', 0)) > 0.01:
            raise forms.ValidationError({'total_applicant_contribution': ['Total applicant contribution does not match calculated total.']})
        if abs(cleaned_data.get('total_estimated_cost', 0) - (cleaned_data.get('total_ivp_contribution', 0) + cleaned_data.get('total_applicant_contribution', 0))) > 0.01:
            raise forms.ValidationError({'total_estimated_cost': ['Total estimated cost must equal the sum of IVP and applicant contributions.']})

        return cleaned_data

class InnovationVoucherFormStep4(forms.Form):
    request_knowledge_partner = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}))




class PatentApplicationFormStep1(forms.ModelForm):
    contact_number = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Please enter a valid 10-digit phone number.")],
        widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'pattern': '[0-9]{10}', 'maxlength': '10'})
    )
    inventor_count = forms.IntegerField(
        min_value=1,
        max_value=10,
        validators=[RegexValidator(r'^\d+$', message="Please enter a valid number of inventors (1-10).")],
        widget=forms.NumberInput(attrs={'class': 'form-control zoom-input', 'min': '1', 'max': '10'})
    )

    class Meta:
        model = PatentApplication
        fields = ['startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 'email', 'contact_number',
                  'company_classification', 'date_of_registration', 'uam_certificate', 'website', 'inventor_count']
        widgets = {
            'date_of_registration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control zoom-input', 'max': timezone.now().strftime('%Y-%m-%d')}),
            'uam_certificate': forms.ClearableFileInput(attrs={'class': 'form-control zoom-input', 'accept': '.ppt,.pptx,.pdf'}),
            'state': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'district': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'startup_name': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'dpiit_number': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'address': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'country': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control zoom-input'}),
            'company_classification': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'website': forms.URLInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].required = False

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Step 1 form data: {cleaned_data}")

        required_fields = ['startup_name', 'dpiit_number', 'address', 'country', 'state', 'district',
                           'email', 'contact_number', 'company_classification', 'date_of_registration',
                           'uam_certificate', 'inventor_count']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        date_of_registration = cleaned_data.get('date_of_registration')
        if date_of_registration and date_of_registration > timezone.now().date():
            self.add_error('date_of_registration', "Date of registration cannot be in the future.")
            logger.error("Validation error: date_of_registration is in the future")

        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")
            logger.error("Validation error: invalid email format")

        website = cleaned_data.get('website')
        if website and not re.match(r'^(https?:\/\/)?([\w\-]+\.)*[\w\-]+(\.[\w\-]+)+([\/\w\.\-\?=&%]*)?$', website):
            self.add_error('website', "Please enter a valid URL (e.g., https://example.com or https://example.com/path).")
            logger.error("Validation error: invalid website URL")

        contact_number = cleaned_data.get('contact_number')
        if contact_number and not re.match(r'^\d{10}$', contact_number):
            self.add_error('contact_number', "Please enter a valid 10-digit phone number.")
            logger.error("Validation error: invalid contact number")

        inventor_count = cleaned_data.get('inventor_count')
        if inventor_count is None or inventor_count < 1 or inventor_count > 10:
            self.add_error('inventor_count', "Please enter a valid number of inventors (1-10).")
            logger.error("Validation error: invalid or missing inventor_count")
        else:
            inventor_count = int(inventor_count)

        cleaned_data['inventors'] = []
        for i in range(1, inventor_count + 1):
            name = self.data.get(f'inventorName{i}')
            designation = self.data.get(f'inventorDesignation{i}')
            dob = self.data.get(f'inventorDOB{i}')
            aadhaar = self.files.get(f'inventorAadhaar{i}')
            mobile = self.data.get(f'inventorMobile{i}')
            email = self.data.get(f'inventorEmail{i}')

            if not all([name, designation, dob, aadhaar, mobile, email]):
                self.add_error(None, f"All details for Inventor {i} are required.")
                logger.error(f"Validation error: Inventor {i} details incomplete")
            elif not re.match(r'^\d{10}$', mobile):
                self.add_error(None, f"Invalid mobile number for Inventor {i}. Must be exactly 10 digits.")
                logger.error(f"Validation error: invalid mobile number for Inventor {i}")
            elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                self.add_error(None, f"Invalid email address for Inventor {i}.")
                logger.error(f"Validation error: invalid email for Inventor {i}")
            elif aadhaar and not aadhaar.name.endswith('.pdf'):
                self.add_error(None, f"Invalid file format for Inventor {i} Aadhaar. Must be a PDF.")
                logger.error(f"Validation error: invalid Aadhaar file format for Inventor {i}")
            else:
                cleaned_data['inventors'].append({
                    'name': name.strip(),
                    'designation': designation.strip(),
                    'dob': dob,
                    'aadhaar': aadhaar,
                    'mobile': mobile.strip(),
                    'email': email.strip()
                })

        uam_certificate = cleaned_data.get('uam_certificate')
        if uam_certificate and not uam_certificate.name.lower().endswith(('.ppt', '.pptx', '.pdf')):
            self.add_error('uam_certificate', "Please upload a valid file (.ppt, .pptx, or .pdf).")
            logger.error("Validation error: invalid uam_certificate file type")

        return cleaned_data

class PatentApplicationFormStep2(forms.ModelForm):
    invention_category = forms.ChoiceField(choices=[('Process', 'Process'), ('Product', 'Product')], required=True)
    stage_of_development = forms.CharField(max_length=50, required=True)
    test_status = forms.ChoiceField(choices=[
        ('Self Tested', 'Self Tested'),
        ('Not Tested', 'Not Tested'),
        ('Tested by Government Agency', 'Tested by Government Agency'),
        ('Tested by Private Agency', 'Tested by Private Agency'),
        ('Tested by Industry', 'Tested by Industry')
    ], required=True)
    patent_status = forms.ChoiceField(choices=[
        ('provisional', 'Filed Provisional Patent'),
        ('complete', 'Filed Complete Patent'),
        ('notFiled', 'Not Filed')
    ], required=True)
    patent_date = forms.DateField(required=False)
    patent_number = forms.CharField(max_length=50, required=False)
    enclosed = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], required=True)
    enclosed_file = forms.FileField(required=False)
    abstract = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    state_of_art = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    drawbacks_overcome = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    objectives = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = PatentApplication
        fields = ['invention_category', 'stage_of_development', 'test_status', 'patent_status', 'patent_date', 'patent_number',
                  'enclosed', 'enclosed_file', 'abstract', 'state_of_art', 'drawbacks_overcome', 'objectives']

    def clean(self):
        cleaned_data = super().clean()
        patent_status = cleaned_data.get('patent_status')
        if patent_status in ['provisional', 'complete']:
            if not cleaned_data.get('patent_date'):
                self.add_error('patent_date', "Patent filed date is required.")
            if not cleaned_data.get('patent_number'):
                self.add_error('patent_number', "Patent number is required.")

        enclosed = cleaned_data.get('enclosed')
        if enclosed == 'Yes':
            if not cleaned_data.get('enclosed_file'):
                self.add_error('enclosed_file', "File upload is required when enclosed is Yes.")

        return cleaned_data

class PatentApplicationFormStep3(forms.ModelForm):
    novel_features = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    advantages = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    detailed_description_file = forms.FileField(required=True)
    reprints_file = forms.FileField(required=True)

    class Meta:
        model = PatentApplication
        fields = ['novel_features', 'advantages', 'detailed_description_file', 'reprints_file']

    def clean(self):
        cleaned_data = super().clean()
        detailed_description_file = cleaned_data.get('detailed_description_file')
        if detailed_description_file and not detailed_description_file.name.lower().endswith(('.pdf', '.jpg', '.png')):
            self.add_error('detailed_description_file', "Please upload a valid file (.pdf, .jpg, or .png).")

        reprints_file = cleaned_data.get('reprints_file')
        if reprints_file and not reprints_file.name.lower().endswith(('.pdf', '.jpg', '.png')):
            self.add_error('reprints_file', "Please upload a valid file (.pdf, .jpg, or .png).")

        return cleaned_data
    

    

class PriorArtSearchFormStep1(forms.ModelForm):
    contact_number = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Please enter a valid 10-digit phone number.")],
        widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'pattern': '[0-9]{10}', 'maxlength': '10'})
    )
    inventor_count = forms.IntegerField(
        validators=[RegexValidator(r'^\d+$', message="Please enter a valid number of inventors (1-10).")],
        widget=forms.TextInput(attrs={'class': 'form-control zoom-input', 'pattern': '[0-9]+', 'maxlength': '2'})
    )

    class Meta:
        model = PriorArtSearch
        fields = [
            'startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 
            'email', 'contact_number', 'company_classification', 'date_of_registration', 
            'uam_certificate', 'website', 'inventor_count'
        ]
        widgets = {
            'date_of_registration': forms.DateInput(attrs={'type': 'date', 'class': 'form-control zoom-input', 'max': timezone.now().strftime('%Y-%m-%d')}),
            'uam_certificate': forms.ClearableFileInput(attrs={'class': 'form-control zoom-input'}),
            'state': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'district': forms.Select(attrs={'class': 'form-select zoom-input'}),
            'website': forms.URLInput(attrs={'class': 'form-control zoom-input', 'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].required = False

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Prior Art Search Step 1 form data: {cleaned_data}")

        # Validate required Step 1 fields (excluding website)
        step1_fields = ['startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 
                        'email', 'contact_number', 'company_classification', 'inventor_count']
        for field in step1_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        # Validate uam_certificate
        if not cleaned_data.get('uam_certificate'):
            self.add_error('uam_certificate', "UAM certificate is required.")
            logger.error("Validation error: uam_certificate is missing")

        # Validate date_of_registration
        date_of_registration = cleaned_data.get('date_of_registration')
        if date_of_registration:
            if date_of_registration > timezone.now().date():
                self.add_error('date_of_registration', "Date of registration cannot be in the future.")
                logger.error("Validation error: date_of_registration is in the future")
        else:
            self.add_error('date_of_registration', "Date of registration is required.")
            logger.error("Validation error: date_of_registration is missing")

        # Validate email format
        email = cleaned_data.get('email')
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            self.add_error('email', "Please enter a valid email address.")
            logger.error("Validation error: invalid email format")

        # Validate website URL if provided
        website = cleaned_data.get('website')
        if website and not re.match(r'^(https?:\/\/)?([\w\-]+\.)*[\w\-]+(\.[\w\-]+)+([\/\w\.\-\?=&%]*)?$', website):
            self.add_error('website', "Please enter a valid URL (e.g., https://example.com or https://example.com/path).")
            logger.error("Validation error: invalid website URL")

        # Validate inventor_count
        inventor_count = cleaned_data.get('inventor_count')
        if inventor_count is None or inventor_count < 1 or inventor_count > 10:
            self.add_error('inventor_count', "Please enter a valid number of inventors (1-10).")
            logger.error("Validation error: invalid or missing inventor_count")
        else:
            inventor_count = int(inventor_count)

        # Store inventor details in cleaned_data for later use
        cleaned_data['inventors'] = []
        for i in range(1, inventor_count + 1):
            name = self.data.get(f'inventorName{i}')
            designation = self.data.get(f'inventorDesignation{i}')
            dob = self.data.get(f'inventorDOB{i}')
            aadhaar = self.files.get(f'inventorAadhaar{i}')
            mobile = self.data.get(f'inventorMobile{i}')
            email = self.data.get(f'inventorEmail{i}')

            if not all([name, designation, dob, aadhaar, mobile, email]):
                self.add_error(None, f"All details for Inventor {i} are required.")
                logger.error(f"Validation error: Inventor {i} details incomplete")
            elif mobile and not re.match(r'^\d{10}$', mobile):
                self.add_error(None, f"Invalid mobile number for Inventor {i}. Must be exactly 10 digits.")
                logger.error(f"Validation error: invalid mobile number for Inventor {i}")
            elif email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                self.add_error(None, f"Invalid email address for Inventor {i}.")
                logger.error(f"Validation error: invalid email for Inventor {i}")
            elif aadhaar and not aadhaar.name.endswith('.pdf'):
                self.add_error(None, f"Invalid file format for Inventor {i} Aadhaar. Must be a PDF.")
                logger.error(f"Validation error: invalid Aadhaar file format for Inventor {i}")
            else:
                cleaned_data['inventors'].append({
                    'name': name.strip(),
                    'designation': designation.strip(),
                    'dob': dob,
                    'aadhaar': aadhaar,
                    'mobile': mobile.strip(),
                    'email': email.strip()
                })

        return cleaned_data

class PriorArtSearchFormStep2(forms.ModelForm):
    class Meta:
        model = PriorArtSearch
        fields = [
            'invention_title', 'abstract', 'scope_invention', 'use_invention', 
            'functional_structure', 'advantage', 'key_features', 
            'known_prior_art', 'major_assignees', 'inventors_search', 'remarks_info'
        ]
        widgets = {
            'invention_title': forms.TextInput(attrs={'class': 'form-control zoom-input'}),
            'abstract': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'scope_invention': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'use_invention': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'functional_structure': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'advantage': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'key_features': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'known_prior_art': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'major_assignees': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'inventors_search': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
            'remarks_info': forms.Textarea(attrs={'rows': 3, 'class': 'form-control zoom-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['known_prior_art', 'major_assignees', 'inventors_search', 'remarks_info']:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        logger.debug(f"Cleaning Step 2 form data: {cleaned_data}")

        required_fields = [
            'invention_title', 'abstract', 'scope_invention', 'use_invention', 
            'functional_structure', 'advantage', 'key_features'
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').title()} is required.")
                logger.error(f"Validation error: {field} is missing")

        return cleaned_data