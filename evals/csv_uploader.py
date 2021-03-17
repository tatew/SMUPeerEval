import csv
from .models import Student
from django.db.utils import IntegrityError
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.contrib import messages

def importCSV(reader, request):
    reader.__next__()
    header = ['lastName', 'firstName', 'email', 'school', 'programme']
    line = 1
    num_imported = 0
    for row in reader:
        row = {header[i]: row[i] for i in range(len(row))}
        try:
            student = Student(**row)
            student.save()
            num_imported += 1
        except:
            messages.error(request, f"Error creating student on line {line}. This student was not created")
        line += 1
    messages.success(request, f"{num_imported} students successfully imported")
    
