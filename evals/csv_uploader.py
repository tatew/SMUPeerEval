import csv
from .models import Student
from django.contrib import messages

def importCSV(reader, request):
    reader.__next__()
    header = ['lastName', 'firstName', 'email', 'school', 'programme']
    line = 1
    num_imported = 0
    num_failed = 0
    for row in reader:
        row = {header[i]: row[i] for i in range(len(row))}
        row['email'] = row['email'].lower()
        if len(row) != 5:
            messages.error(request, f"Error creating student on line {line}. This student was not created")
            num_failed += 1
        else:
            try:
                student = Student(**row)
                student.save()
                num_imported += 1
            except:
                messages.error(request, f"Error creating student on line {line}. This student was not created")
                num_failed += 1
            line += 1
    if num_imported > 0:
        messages.success(request, f"{num_imported} students successfully imported")
    if num_failed > 0:
        messages.error(request, f"{num_failed} students failed to import")


    
