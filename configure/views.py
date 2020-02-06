from django.shortcuts import render
import meraki
import os
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect

def apicheck(request):
    if request.user.is_authenticated:
        my_orgs = ''
        GetOrgList = ''
        if 'apikey' in request.GET: 
            api_key = request.GET['apikey']
            if not api_key == '':
                dashboard = meraki.DashboardAPI(
                api_key = api_key,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
                my_orgs = dashboard.organizations.getOrganizations()
                org_id = []
                org_name = []
                for org in my_orgs:
                    org_id.append(org["id"])
                    org_name.append(org["name"])
                table = zip(org_name,org_id)    
        return render(request, 'tools.html', {'table':table})
        
        
        
        if 'GetOrgList' in request.GET: 
            api_key = request.GET['batchget']
            organizationId = request.GET['orgid']
            if not api_key == '' & organizationId == '' :
                dashboard = meraki.DashboardAPI(
                api_key = api_key,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
                batchlist = dashboard.action_batches.getOrganizationActionBatches()
        return render(request, 'tools.html', {'batch':batchlist})
    else:
        return redirect('/')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'confhome.html')
    else:
        return redirect('/')
 
#def bulk(request):
