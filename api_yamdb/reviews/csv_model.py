from urllib import request
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import (
    Categories,
    Genres,
    Titles,
    Review,
    CustomUser,
    Comment,)

def Categories_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = Categories.objects.get_or_create(
                id=fields[0],
                name=fields[1],
                slug=fields[2],
            )
        question.save()
    except Exception as e:
            #messages.error(request, "Unable to upload file. "+repr(e))
            pass

def Genres_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = Genres.objects.get_or_create(
                name=fields[1],
                slug=fields[2],
            )
        question.save()
    except Exception as e:
            messages.error(request, "Unable to upload file. "+repr(e))
    pass

def Titles_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = Titles.objects.get_or_create(
                id=fields[0],
                name=fields[1],
                year=fields[2],
                #description=fields[2],
                category=fields[3],
                #genre=fields[2],
            )
        question.save()
    except Exception as e:
        #messages.error(request, "Unable to upload file. "+repr(e))
        pass


def Review_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = Review.objects.get_or_create(
                id=fields[0],
                title_id=fields[1],
                text=fields[2],
                author=fields[3],
                score=fields[4],
                pub_date=fields[5],
                
            )
        question.save()
    except Exception as e:
            #messages.error(request, "Unable to upload file. "+repr(e))
        pass

def CustomUser_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = CustomUser.objects.get_or_create(
                id=fields[0],
                username=fields[1],
                email=fields[2],
                role=fields[3],
                bio=fields[4],
                first_name=fields[5],
                last_name=fields[6],
                
            )
        question.save()
    except Exception as e:
            #messages.error(request, "Unable to upload file. "+repr(e))
        pass


def Comment_csv(lines):
    try:
        for line in lines:
            fields = line.split(",")
            question = Comment.objects.get_or_create(
                id=fields[0],
                title_id=fields[1],
                text=fields[2],
                author=fields[3],
                score=fields[4],
                pub_date=fields[5],
                
            )
        question.save()
    except Exception as e:
            #messages.error(request, "Unable to upload file. "+repr(e))
        pass
