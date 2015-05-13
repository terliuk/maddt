# Create your views here.
from django.shortcuts import render_to_response 
from django.template import loader,Context,RequestContext 
from django.http import HttpResponse, HttpResponseRedirect 


from django.views import generic

from models import CopyJob

import numpy as n

# generic model views
class IndexView(generic.ListView):
    template_name = 'copyjobs/index.html'
    context_object_name = 'copyjobs_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return CopyJob.objects.order_by('-transfertime')[:10]


class DetailView(generic.DetailView):
    model = CopyJob
    template_name = 'copyjobs/detail.html'


# some graphic stuf
def jobstatistics(request):
    jobs = CopyJob.objects.all()
    times      = [job.elapsed_time/60. for job in jobs] # minutes
    datavolume = [job.datavolume/1000000. for job in jobs] # megabytes  
    volume_bins = n.linspace(0,1000000,50)
    time_bins   = n.linspace(0,2880,50)
    hist_d = n.histogram(datavolume,bins=volume_bins)
    hist_t = n.histogram(times,bins=time_bins)
    print hist_d
    print hist_t

    content = dict()
    content["volume_bins"] = [int(b) for b in volume_bins]
    content["time_bins"]   = [int(b) for b in time_bins]
    content["volume_data"] = list(hist_d[0])
    content["time_data"]   = list(hist_t[0])
    return render_to_response("copyjobs/statistics.html",content,context_instance=RequestContext(request))



