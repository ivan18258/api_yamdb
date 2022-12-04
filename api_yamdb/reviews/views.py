from django.http import HttpResponseRedirect
import re
import csv
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .csv_model1 import (
    Categories_csv,
    Genres_csv,
    Titles_csv,
    Review_csv,
    CustomUser_csv,
    Comment_csv,
)

def upload_csv(request):
    list_files={
        'category.csv':Categories_csv,
        'genre.csv':Genres_csv,
        'titles.csv':Titles_csv,
        'review.csv':Review_csv,
        'users.csv':CustomUser_csv,
        'comments.csv':Comment_csv,
        }
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Загрузите файл формата CSV')
            return HttpResponseRedirect(reverse("reviews:upload_csv"))

        if not csv_file.name in list_files:
            messages.error(request, 'Не угадал, попробуй ещё!')
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        # if file is too large - error
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        a=lines.pop(0)

        for line in lines:
            fielde = line.split(',')
            list_files[csv_file.name](fielde)
        """with csv_file.read().decode("utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                list_files[request.FILES["csv_file"].name].objects.bulk_create ([row])"""

    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("reviews:upload_csv"))



"""
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not a CSV')
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        # if file is too large - error
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("reviews:upload_csv"))
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        # loop over the lines and save them to db via model
        for line in lines:
            fields = line.split(",")
            try:
                question = Genres(
                    name=fields[1],
                    slug=fields[2],
                )
                question.save()
            except Exception as e:
                messages.error(request, "Unable to upload file. "+repr(e))
                pass
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("reviews:upload_csv"))"""