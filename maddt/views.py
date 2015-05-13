from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response 
from django.template import loader,Context,RequestContext 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.views import logout
from django.conf import settings

from os import mkdir
from os.path import join

import os
import re


from django.db.models import F
from gridcopy.models import Urlpath as Urlpath
from copyjobs.models import CopyJob


def home(request):
    """
    test implementation: show the last 10 copied files
    """
    c = dict()
    if request is None:
        return HtmlResponse("not implemented yet!")
    else:
        return render_to_response("home.html",c,context_instance=RequestContext(request))




def madison_database_overview(request):
    """
    Show how much is copied from the database 
    """
    x = Urlpath.objects.all()[:1]
    DATASET=1871
    bs_run_pattern = re.compile(r"_Run[0-9]{7}0")
    bs_run_pattern = r"_Run[0-9]{7}0"
    content = dict()
    for datatype in ("Level2","PFFilt"):
        all_files    = Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).count()    
        copied_files = Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(transferstate__exact="TRANSFERRED").count()   
        copied_percentage = 0
        content["percentage_copied_" + datatype] = 0.
        if copied_files:    
            copied_percentage = 100*float(copied_files)/all_files

        content["percentage_copied_" + datatype] = 100*float(copied_files)/all_files

        if datatype == "Level2": #no extra gcd for PFFilt
            # filter out all 0 ending runs for the bs
            all_files_gcd =  Urlpath.objects.filter(name__contains=datatype).filter(name__contains="GCD").filter(dataset_id__exact=DATASET).count()
            copied_files_gcd = Urlpath.objects.filter(name__contains=datatype).filter(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(transferstate__exact="TRANSFERRED").count()  

            copied_percentage = 0
            content["percentage_copied_gcd_" + datatype] = 0.
            if copied_files_gcd:    
                copied_percentage = 100*float(copied_files_gcd)/all_files_gcd
 
            content["percentage_copied_gcd_" + datatype] = copied_percentage

        all_files_bs =  Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(name__regex=bs_run_pattern).count()
        copied_files_bs = Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(name__regex=bs_run_pattern).filter(transferstate__exact="TRANSFERRED").count()  

        copied_percentage = 0
        content["percentage_copied_bs_" + datatype] = 0.
        if copied_files_bs:
            copied_percentage = 100*float(copied_files_bs)/all_files_bs
    
        content["percentage_copied_bs_" + datatype] = copied_percentage
        
        content["percentage_copied_month_" + datatype] = []
        for month in [str(mth).zfill(2) for mth in xrange(1,13)]:
            all_files    = Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(path__contains="level2/" + month).count()    
            copied_files = Urlpath.objects.filter(name__contains=datatype).exclude(name__contains="GCD").filter(dataset_id__exact=DATASET).filter(path__contains="level2/" + month).filter(transferstate__exact="TRANSFERRED").count()    
            copied_percentage = 0
            if copied_files:   
                copied_percentage = float(copied_files)/all_files 
            content["percentage_copied_month_" + datatype].append(100*copied_percentage)
    print content
 
    return render_to_response("madison_database_overview.html",content,context_instance=RequestContext(request))

