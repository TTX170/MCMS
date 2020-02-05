from django.shortcuts import render
import meraki
import os
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect

def apicheck(request):
    if request.user.is_authenticated:
        my_orgs = {}
        if 'apikey' in request.GET: 
            api_key = request.GET['apikey']
            dashboard = meraki.DashboardAPI(
            api_key = api_key,
            base_url='https://api-mp.meraki.com/api/v0/',
            log_file_prefix=os.path.basename(__file__)[:-3],
            print_console=False
            )
            my_orgs = dashboard.organizations.getOrganizations()
        return render(request, 'tools.html', {'org':my_orgs})
    else:
        return redirect('/')
   