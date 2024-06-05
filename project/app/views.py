from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
from django.core.mail import send_mail

def file_upload(request):
    if request.method == "POST":
        file = request.FILES['file']

        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return render(request, 'upload.html', {'error': 'File format not supported'})
        
        request.session['data'] = df.to_dict()
        return HttpResponseRedirect('/summary/')
    
    return render(request, 'upload.html')




def report_summary(request):
    data = request.session.get('data')
    if data:
        df = pd.DataFrame(data)

        
        column_names = list(df.columns)

       
        summary = df.groupby(column_names).size().reset_index(name='Count')

     
        summary = summary.sort_values(by=column_names)

        summary_html = summary.to_html(index=False)

        subject = 'Summary Report'
        message = 'Here is the summary report:\n\n' + summary_html
        email_from = 'testing20044@gmail.com'
        recipient_list = ['tech@themedius.ai', 'hr@themedius.ai']
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        return render(request, 'summary.html', {'summary': summary_html})

    return HttpResponseRedirect('/')