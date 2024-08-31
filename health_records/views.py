from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import HealthRecord

@csrf_protect
def reception_view(request):
    if request.method == 'POST':
        # Get the current user (assuming user is logged in)
        user = request.user
        
        if user.is_authenticated:
            insurance_details = request.POST.get('insuranceDetails')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            age = request.POST.get('age')

            try:
                # Create and save a new HealthRecord instance
                health_record = HealthRecord(
                    user=user,
                    insurance_details=insurance_details,
                    height=height,
                    weight=weight,
                    age=age,
                )
                health_record.save()

                # Add a success message to the messages framework
                messages.success(request, 'Data received and saved successfully.')

                # Redirect to the patient dashboard page
                return redirect('patient_dashboard')

            except Exception as e:
                # Handle any errors that may occur
                messages.error(request, f'Error: {str(e)}')
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'User not authenticated')
            return redirect('patient_dashboard')
    
    return redirect('patient_dashboard')  # Redirect in case of invalid request method


