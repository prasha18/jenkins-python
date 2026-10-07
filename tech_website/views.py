from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Technology, Sector
from techforms.models import Patent

def home(request):
    return render(request, 'tech_website/index.html')

def about(request):
    return render(request, 'tech_website/about.html')

def programs(request):
    return render(request, 'tech_website/programs.html')

def technology(request):
    sector_filter = request.GET.get('sector', '')
    
    technologies = Technology.objects.all()
    if sector_filter:
        technologies = technologies.filter(sector__name=sector_filter)
    
    patents = Patent.objects.filter(is_approved=True)
    if sector_filter:
        patents = patents.filter(sector__name=sector_filter)
    
    combined_items = []
    for tech in technologies:
        combined_items.append({
            'unique_id': tech.unique_id,
            'title': tech.title,
            'description': tech.description,
            'pdf': tech.pdf,
            'type': 'Technology',
            'sort_date': tech.created_at
        })
    for patent in patents:
        combined_items.append({
            'unique_id': patent.unique_id,
            'title': patent.title,
            'description': patent.description,
            'pdf': patent.pdf_write,
            'type': 'Patent',
            'sort_date': patent.approved_at if patent.approved_at else patent.created_at
        })
    
    combined_items.sort(key=lambda x: x['sort_date'], reverse=True)
    
    paginator = Paginator(combined_items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    sectors = Sector.objects.all()
    context = {
        'page_obj': page_obj,
        'sectors': sectors,
        'sector_filter': sector_filter,
    }
    return render(request, 'tech_website/technology.html', context)

def technology_transfer(request):
    return render(request, 'tech_website/technology-transfer.html')

def ipmanagement(request):
    return render(request, 'tech_website/ipmanagement.html')

def spinoff_support(request):
    return render(request, 'tech_website/spinoff-support.html')

def seedgrant(request):
    return render(request, 'tech_website/seedgrant.html')

def trl_assessment(request):
    return render(request, 'tech_website/trl-assessment.html')

def contact(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not all([name, email, phone, message]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'tech_website/contactus.html')
        # Prepare email
        subject = f'Enquiry From TNTTFC'
        body = f"""
        New inquiry received:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """
        recipient_list = ['Developer@tnthub.org', 'daniel@tnthub.org']
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your message has been sent successfully. We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        return redirect('contactus')
    return render(request, 'tech_website/contactus.html')

def services(request):
    return render(request, 'tech_website/services.html')

def tech_showcase(request):
    return render(request, 'tech_website/tech-showcase.html')