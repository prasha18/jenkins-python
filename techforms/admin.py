from django.contrib import admin
from .models import InnovationVoucherApplication, PatentApplication, PriorArtSearch, TrademarkApplication, TRLAssessment, ExpressInterest, Patent


@admin.register(ExpressInterest)
class ExpressInterestAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'organization_name', 'email', 'patent_title', 'area_of_interest', 'created_at')
    list_filter = ('created_at', 'area_of_interest', 'location')
    search_fields = ('applicant_name', 'organization_name', 'email', 'patent_title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'applicant_name', 'email', 'sector', 'state', 'district', 'is_approved', 'unique_id', 'created_at')
    list_filter = ('is_approved', 'sector', 'state', 'district', 'created_at')
    search_fields = ('title', 'applicant_name', 'email', 'description', 'unique_id')
    ordering = ('-created_at',)
    list_per_page = 25
    readonly_fields = ('created_at', 'unique_id')
    list_editable = ('is_approved',)
    actions = ['approve_patents', 'disapprove_patents']
    fieldsets = (
        ('Personal Information', {
            'fields': ('applicant_name', 'email', 'contact_number', 'address', 'country', 'state', 'district')
        }),
        ('Patent Details', {
            'fields': ('title', 'description', 'sector', 'pdf_write', 'word_write', 'is_approved', 'unique_id')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

    def approve_patents(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected patents have been approved.")
    approve_patents.short_description = "Approve selected patents"

    def disapprove_patents(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected patents have been disapproved.")
    disapprove_patents.short_description = "Disapprove selected patents"



@admin.register(InnovationVoucherApplication)
class InnovationVoucherApplicationAdmin(admin.ModelAdmin):
    list_display = ('startup_name', 'dpiit_number', 'email', 'contact_number', 'company_classification', 'director_count', 'voucher_type', 'created_at')
    list_filter = ('company_classification', 'voucher_type', 'date_of_registration', 'country')
    search_fields = ('startup_name', 'dpiit_number', 'email', 'contact_number', 'project_title')
    date_hierarchy = 'date_of_registration'
    ordering = ('-created_at',)
    fields = (
        'startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 'email', 
        'contact_number', 'company_classification', 'date_of_registration', 'uam_certificate', 
        'turnover', 'website', 'director_count', 'voucher_type', 'project_title', 
        'product_name', 'problem_statement', 'solution_proposed', 'detailed_description', 
        'invention_upgrade', 'scope', 'need', 'competitive_advantage', 'social_impact', 
        'collaboration', 'benefits', 'price_advantage', 'project_cost', 'target_dates', 
        'ppt_upload', 'youtube_link', 
        'outsourcing_charges', 'outsourcing_ivp', 'outsourcing_applicant',
        'raw_materials', 'raw_ivp', 'raw_applicant',
        'fabrication_charges', 'fabrication_ivp', 'fabrication_applicant',
        'ipr_patent', 'ipr_ivp', 'ipr_applicant',
        'testing_validation', 'testing_ivp', 'testing_applicant',
        'commercialization_support', 'commercialization_ivp', 'commercialization_applicant',
        'other1_activity', 'other1_cost', 'other1_ivp', 'other1_applicant',
        'other2_activity', 'other2_cost', 'other2_ivp', 'other2_applicant',
        'total_estimated_cost', 'total_ivp_contribution', 'total_applicant_contribution',
        'request_knowledge_partner', 'created_at'
    )
    readonly_fields = ('created_at',)
    change_list_template = "admin/techforms/innovationapplication/change_list.html"
    

@admin.register(PatentApplication)
class PatentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'startup_name', 'dpiit_number', 'date_of_registration', 'email', 
        'contact_number', 'company_classification', 'inventor_count', 'created_at'
    )
    list_filter = ('company_classification', 'date_of_registration', 'country')
    search_fields = ('startup_name', 'dpiit_number', 'email', 'contact_number')
    date_hierarchy = 'date_of_registration'
    fields = (
        'startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 
        'email', 'contact_number', 'company_classification', 'date_of_registration', 
        'uam_certificate', 'website', 'inventor_count', 
        'invention_category', 'stage_of_development', 'test_status', 'patent_status', 
        'patent_date', 'patent_number', 'enclosed', 'enclosed_file', 'abstract', 
        'state_of_art', 'drawbacks_overcome', 'objectives', 'novel_features', 
        'advantages', 'detailed_description_file', 'reprints_file', 'created_at'
    )
    readonly_fields = ('created_at',)
    
    
@admin.register(PriorArtSearch)
class PriorArtSearchAdmin(admin.ModelAdmin):
    list_display = ('startup_name', 'dpiit_number', 'date_of_registration', 'email', 'contact_number', 'company_classification', 'inventor_count', 'created_at')
    list_filter = ('company_classification', 'date_of_registration', 'country')
    search_fields = ('startup_name', 'dpiit_number', 'email', 'contact_number', 'invention_title')
    date_hierarchy = 'date_of_registration'
    
    # FIXED: Removed 'inventor_details' — this field does NOT exist in the model
    fields = ('startup_name', 'dpiit_number', 'address', 'country', 'state', 'district', 'email', 'contact_number', 'company_classification', 'date_of_registration', 'uam_certificate', 'website', 'inventor_count', 'invention_title', 'abstract', 'scope_invention', 'use_invention', 'functional_structure', 'advantage', 'key_features', 'known_prior_art', 'major_assignees', 'inventors_search', 'remarks_info', 'created_at')
    
    readonly_fields = ('created_at',)
    change_list_template = "admin/techforms/priorartapplication/change_list.html"



@admin.register(TRLAssessment)
class TRLAssessmentAdmin(admin.ModelAdmin):
    list_display = ('inventor_name', 'organisation', 'email', 'contact_number', 'technology_title', 'created_at')
    list_filter = ('created_at', 'organisation')
    search_fields = ('inventor_name', 'organisation', 'email', 'technology_title')
    ordering = ('-created_at',)
    fields = ('inventor_name', 'organisation', 'email', 'contact_number', 'technology_title', 
              'field_of_invention', 'technology_description', 'market_segment', 'patent_details', 'created_at')
    readonly_fields = ('created_at',)



    


@admin.register(TrademarkApplication)
class TrademarkApplicationAdmin(admin.ModelAdmin):
    list_display = ('startup_name', 'dpiit_number', 'date_of_registration', 'email', 'contact_number', 'company_classification', 'inventor_count', 'slogan', 'created_at')
    list_filter = ('company_classification', 'date_of_registration', 'country')
    search_fields = ('startup_name', 'dpiit_number', 'email', 'contact_number', 'slogan')
    date_hierarchy = 'date_of_registration'





