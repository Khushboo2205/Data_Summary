import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

def handle_uploaded_file(f):
    # Read the uploaded file
    if f.name.endswith('.csv'):
        data = pd.read_csv(f)
    else:
        data = pd.read_excel(f)
    
    # Check if required columns exist
    required_columns = ['State', 'DPD']
    if not all(column in data.columns for column in required_columns):
        raise ValueError(f"Uploaded file must contain the following columns: {', '.join(required_columns)}")
    
    # Generate the summary report
    summary = data.groupby(['State', 'DPD']).size().reset_index(name='Count')
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                summary = handle_uploaded_file(request.FILES['file'])
                return render(request, 'upload/result.html', {'summary': summary.to_html()})
            except ValueError as e:
                return render(request, 'upload/upload.html', {'form': form, 'error': str(e)})
            except Exception as e:
                return render(request, 'upload/upload.html', {'form': form, 'error': 'An unexpected error occurred. Please try again.'})
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})