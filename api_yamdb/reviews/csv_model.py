from urllib import request
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import (
    Categories,
    Genres,
    Title,
    Review,
    CustomUser,
    Comment,)

def Categories_csv(fields):
    return Categories(
                id=fields[0],
                name=fields[1],
                slug=fields[2],
            )


def Genres_csv(fields):
        Genres.objects.get_or_create(
            name=fields[1],
            slug=fields[2],
        )
pass
 

def Titles_csv(fields):
    Title.objects.get_or_create(
        id=int(fields[0]),
        name=fields[1],
        year=int(fields[2]),
                #description=fields[2],
        category_id=int(fields[3]),
                #genre=fields[2],
    )
pass



def Review_csv(fields):
    Review.objects.get_or_create(
                id=fields[0],
                title_id=fields[1],
                text=fields[2],
                author=fields[3],
                score=fields[4],
                pub_date=fields[5],
                
            )
pass


def CustomUser_csv(fields):
    CustomUser.objects.get_or_create(
            #id=fields[0],
            username=fields[1],
            email=fields[2],
            role=fields[3],
            bio=fields[4],
            first_name=fields[5],
            last_name=fields[6]
            )
#        question.save()
   # pass



def Comment_csv(fields):

    return Comment(
        id=fields[0],
        review_id=fields[1],
        text=fields[2],
        author=fields[3],
            #score=fields[4],
        pub_date=fields[4],
                
        )
    