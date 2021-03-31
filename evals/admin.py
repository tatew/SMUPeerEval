from django.contrib import admin, messages
from django.urls import path

from .models import Course, Professor, Student, Group, Category, Score, AssessmentAssigned, AssessmentSubmitted
from django import forms
from django.http import HttpResponseRedirect

from evals.csv_uploader import importCSV
import csv

import io
# Register your models here.
admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Group)
admin.site.register(Category)

#REMOVE THESE LATER!
admin.site.register(Score)
admin.site.register(AssessmentAssigned)
admin.site.register(AssessmentSubmitted)

class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()

class CsvUploadAdmin(admin.ModelAdmin):

    change_list_template = "evals/importCSV.html"

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = CsvUploadForm()
        return super(CsvUploadAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == 'POST':
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if request.FILES['csv_file'].name.endswith('csv'):

                    try:
                        decoded_file = request.FILES['csv_file'].read().decode('utf-8')
                    except UnicodeDecodeError as e:
                        messages.error(
                            request,
                            "There was an error decoding the file:{}".format(e)
                        )
                        return redirect("..")
                    
                    io_string = io.StringIO(decoded_file)
                    csvReader = csv.reader(io_string, delimiter=',')
                    importCSV(csvReader, request)

                else:
                    messages.error(
                        request,
                        "Incorrect file type: {}".format(
                            request.FILES['csv_file'].name.split(".")[1]
                        )
                    )

            else:
                messages.error(
                    request,
                    "There was an error in the form {}".format(form.errors)
                ) 

        return HttpResponseRedirect("..")

@admin.register(Student)
class StudentAdmin(CsvUploadAdmin):
    pass