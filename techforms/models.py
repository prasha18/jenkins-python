from django.db import models
from django.contrib.postgres.fields import JSONField
import json
from tech_repo.models import State, District
from django.core.validators import MinLengthValidator
from tech_website.models import Sector
import random
import string
from django.utils import timezone


def generate_custom_id():
    def generate_unique_id():
        while True:
            prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            new_id = f"{prefix}{suffix}"
            if not Patent.objects.filter(unique_id=new_id).exists():
                return new_id
    return generate_unique_id()

class Patent(models.Model):
    applicant_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf_write = models.FileField(upload_to='patents/pdf/', blank=True, null=True)
    word_write = models.FileField(upload_to='patents/word/', blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    unique_id = models.CharField(max_length=6, unique=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = generate_custom_id()
        if self.is_approved and not self.approved_at:
            if self.pk:
                try:
                    old_instance = Patent.objects.get(pk=self.pk)
                    if not old_instance.is_approved:
                        self.approved_at = timezone.now()
                except Patent.DoesNotExist:
                    pass
            else:
                self.approved_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ExpressInterest(models.Model):
    applicant_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        help_text="Must be exactly 10 digits."
    )
    organization_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    patent_title = models.CharField(max_length=255)
    area_of_interest = models.CharField(max_length=255) 
    location = models.CharField(max_length=100)
    reason = models.TextField(max_length=5000, blank=True)  
    notes = models.TextField(max_length=5000, blank=True)
    agree_to_contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.patent_title} - Express Interest"





class TRLAssessment(models.Model):
    inventor_name = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        help_text="Must be exactly 10 digits."
    )
    technology_title = models.CharField(max_length=255)
    field_of_invention = models.CharField(max_length=255)
    technology_description = models.TextField(max_length=5000)
    market_segment = models.CharField(max_length=255)
    patent_details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventor_name} - {self.technology_title} - TRL Assessment"

from django.db import models
from tech_repo.models import State, District

class InnovationVoucherApplication(models.Model):
    # Personal Information (Step 1)
    startup_name = models.CharField(max_length=255)
    dpiit_number = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10)
    company_classification = models.CharField(max_length=100)
    date_of_registration = models.DateField()
    uam_certificate = models.FileField(upload_to='uam_certificates/')
    turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    director_count = models.PositiveIntegerField()

    # Project Details (Step 2)
    voucher_type = models.CharField(max_length=1, choices=[('A', 'Voucher A'), ('B', 'Voucher B')])
    project_title = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    problem_statement = models.TextField(max_length=5000)
    solution_proposed = models.TextField(max_length=5000)
    detailed_description = models.TextField(max_length=5000)
    invention_upgrade = models.TextField(max_length=5000)
    scope = models.TextField(max_length=5000)
    need = models.TextField(max_length=5000)
    competitive_advantage = models.TextField(max_length=5000)
    social_impact = models.TextField(max_length=5000)
    collaboration = models.TextField(max_length=5000)
    benefits = models.TextField(max_length=5000)
    price_advantage = models.TextField(max_length=5000)
    project_cost = models.TextField(max_length=5000)
    target_dates = models.TextField(max_length=10000)
    ppt_upload = models.FileField(upload_to='ppt_presentations/')
    youtube_link = models.URLField(blank=True, null=True)

    # Project Milestone / Activity (Step 3)
    # Outsourcing Charges, R&D, Consultancy, Engineering Design Work
    outsourcing_charges = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    outsourcing_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    outsourcing_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Raw materials / Consumables / Spares
    raw_materials = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    raw_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    raw_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Fabrication / Manufacturing charges for POC & Prototype Development
    fabrication_charges = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fabrication_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fabrication_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Intellectual Property Rights / Patent Filing
    ipr_patent = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ipr_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ipr_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Testing and Validation / Laboratory Verification / Certification
    testing_validation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    testing_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    testing_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Commercialisation Support Services
    commercialization_support = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    commercialization_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    commercialization_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Others 1
    other1_activity = models.CharField(max_length=255, null=True, blank=True)
    other1_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other1_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other1_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Others 2
    other2_activity = models.CharField(max_length=255, null=True, blank=True)
    other2_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other2_ivp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other2_applicant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Totals
    total_estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_ivp_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_applicant_contribution = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Request For Knowledge Partner (Step 4)
    request_knowledge_partner = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Innovation Voucher Application"
        verbose_name_plural = "Innovation Voucher Applications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.startup_name} - {self.project_title}"

    @property
    def directors(self):
        """Get all directors associated with this application"""
        from tech_repo.models import Tech_Director
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        return Tech_Director.objects.filter(content_type=content_type, object_id=self.pk)

class PatentApplication(models.Model):
    startup_name = models.CharField(max_length=255)
    dpiit_number = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    contact_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        help_text="Must be exactly 10 digits."
    )
    company_classification = models.CharField(max_length=50)
    date_of_registration = models.DateField()
    uam_certificate = models.FileField(upload_to='certificates/')
    inventor_count = models.PositiveIntegerField()
    invention_category = models.CharField(max_length=7, choices=[('Process', 'Process'), ('Product', 'Product')], null=True)
    stage_of_development = models.CharField(max_length=50, null=True)
    test_status = models.CharField(max_length=50)
    patent_status = models.CharField(max_length=50)
    patent_date = models.DateField(null=True, blank=True)
    patent_number = models.CharField(max_length=50, null=True, blank=True)
    enclosed = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    enclosed_file = models.FileField(upload_to='enclosed_files/', null=True, blank=True)
    abstract = models.TextField()
    state_of_art = models.TextField()
    drawbacks_overcome = models.TextField()
    objectives = models.TextField()
    novel_features = models.TextField()
    advantages = models.TextField()
    detailed_description_file = models.FileField(upload_to='detailed_descriptions/')
    reprints_file = models.FileField(upload_to='reprints/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.startup_name

class PriorArtSearch(models.Model):
    startup_name = models.CharField(max_length=255)
    dpiit_number = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    contact_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        help_text="Must be exactly 10 digits."
    )
    company_classification = models.CharField(max_length=100)
    date_of_registration = models.DateField()
    uam_certificate = models.FileField(upload_to='uam_certificates/')
    website = models.URLField(null=True, blank=True)
    inventor_count = models.PositiveIntegerField()
    invention_title = models.CharField(max_length=255)
    abstract = models.TextField(max_length=5000)
    scope_invention = models.TextField(max_length=5000)
    use_invention = models.TextField(max_length=5000)
    functional_structure = models.TextField(max_length=5000)
    advantage = models.TextField(max_length=5000)
    key_features = models.TextField(max_length=5000)
    known_prior_art = models.TextField(max_length=5000, null=True, blank=True)
    major_assignees = models.TextField(max_length=5000, null=True, blank=True)
    inventors_search = models.TextField(max_length=5000, null=True, blank=True)
    remarks_info = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.startup_name} - Prior Art Search"
    
    

class TrademarkApplication(models.Model):
    startup_name = models.CharField(max_length=255)
    dpiit_number = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    contact_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        help_text="Must be exactly 10 digits."
    )
    company_classification = models.CharField(max_length=100)
    date_of_registration = models.DateField(null=True, blank=True)
    uam_certificate = models.FileField(upload_to='uam_certificates/')
    website = models.URLField(null=True, blank=True)
    inventor_count = models.PositiveIntegerField()
    slogan = models.TextField(max_length=5000)
    color_combination = models.TextField(max_length=5000)
    three_dimensional_mark = models.TextField(max_length=5000)
    class_details = models.TextField(max_length=5000)
    trademark_image = models.FileField(upload_to='trademark_images/')
    trademark_status = models.TextField(max_length=5000, default='NA')
    proof_of_use = models.FileField(upload_to='trademark_proofs/', null=True, blank=True)
    duration_of_use = models.TextField(max_length=5000, default='NA')
    supporting_proof = models.FileField(upload_to='trademark_supporting_proofs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.startup_name} - Trademark Application"