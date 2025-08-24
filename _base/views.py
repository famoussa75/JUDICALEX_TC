from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, '_base/index.html')

