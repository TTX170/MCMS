from django.shortcuts import render, redirect
import meraki, os, io, csv
from django.contrib import messages
from .models import bulk
# Create your views here.

from django.http import HttpResponse
#from django.shortcuts import redirect

def apicheck(request):
    if request.user.is_authenticated:
        my_orgs = ''
        GetOrgList = ''
        table = []
        NetList = ''
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
            return render(request, 'tools.html', {'orgtable':table})
        if 'NetList' in request.GET: 
            api_key = request.GET['NetList']
            organizationId = request.GET['orgid']
            search = request.GET['search']
            result = ''
            netnum = 800
            if not api_key == '':
                dashboard = meraki.DashboardAPI(
                api_key = api_key,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
                my_nets = dashboard.networks.getOrganizationNetworks(organizationId)
                net_id = []
                net_name = []
                net_type = []
                for net in my_nets:
                    net_id.append(net["id"])
                    net_name.append(net["name"])
                    net_type.append(net["type"])
                table = zip(net_name,net_id,net_type) 
                if not search =='':
                    if search in net_name:
                        netnum = net_name.index(search)
                        result = net_id[netnum]      
                    else:
                        result = 'Sorry that ID could not be found'
                    
                    
            return render(request, 'tools.html', {'nettable':table, 'result':result})     
         
       
        if 'batchget' in request.GET: 
            api_key = request.GET['batchget']
            organizationId = request.GET['orgid']
            batchlist = '1'
            if not api_key == '' :
                dashboard = meraki.DashboardAPI(
                api_key = api_key,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
               # batchlist = api_key
                batchlist = dashboard.networks.getOrganizationNetworks(organizationId)
                #batchlist = dashboard.action_batches.getOrganizationActionBatches()
            return render(request, 'tools.html', {'batch':batchlist})
        return render(request, 'tools.html')
    else:
        return redirect('/')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'confhome.html')
    else:
        return redirect('/')
 
def bulkchange(request):
    if request.user.is_authenticated:
            PullTest = bulk.objects.filter(owner=request.user.id)                      
            my_orgs = ''
            GetOrgList = ''
            table=[]
            SearchList=[]
            NetID=0
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
                    net_name = []
                    net_id = []
                    for org in my_orgs:
                        org_id.append(org["id"])
                        org_name.append(org["name"])
                    table = zip(org_name,org_id)                       
                if 'orgID' in request.GET:
                    orgID = request.GET['orgID']
                    my_nets = dashboard.networks.getOrganizationNetworks(orgID)
                    for net in my_nets:
                        net_id.append(net["id"])
                        net_name.append(net["name"])                     
                    for i in PullTest:
                        if i.networkname in net_name:
                            NetID = net_name.index(i.networkname)
                            SearchList.append(net_id[NetID])
                        else:
                            SearchList.append('?')                          
                    
                return render(request, 'bulkchange.html', {'table':table,'pull':PullTest,'search':SearchList})
            data = bulk.objects.all()
            prompt = {
                'order': 'The Serial and Network name fields are required. The following fields are supported: Name, Tags, Notes, Address, Static IP, Netmask, Gateway, DNS1, DNS2, VLAN, Network tags.',
                'profiles': data
                }
                           
            if 'csvfile' in request.FILES:
                csv_file = request.FILES['csvfile']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'THIS IS NOT A CSV FILE')
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    created = bulk.objects.update_or_create(
                        serial = column[0],
                        networkname = column[1],
                        name = column[2],
                        tags = column[3],
                        notes = column[4],
                        address = column[5],
                        ip = column[6],
                        gw = column[7],
                        mask = column[8],
                        dns1 = column[9],
                        dns2 = column[10],
                        vlan = column[11],
                        nettags = column[12],
                        owner = request.user,
                    ) 
                       
                context = {}
                return render(request,'bulkchange.html', context)
            if 'validate' in request.GET:
                changes = bulk.objects.filter(owner=request.user.id)
                api_key = request.GET['apikey']
                orgID = request.GET['orgID']                
                if not (apikey=='' and orgID==''):
                    dashboard = meraki.DashboardAPI(
                    api_key = api_key,
                    base_url='https://api-mp.meraki.com/api/v0/',
                    log_file_prefix=os.path.basename(__file__)[:-3],
                    print_console=False
                    )
                    my_orgs = dashboard.organizations.getOrganizations()
                    org_id = []
                    org_name = []
                    net_name = []
                    net_id = []
                    for org in my_orgs:
                        org_id.append(org["id"])
                        org_name.append(org["name"])
                    my_nets = dashboard.networks.getOrganizationNetworks(orgID)
                    for net in my_nets:
                        net_id.append(net["id"])
                        net_name.append(net["name"])                     
                    for i in PullTest:
                        if i.networkname in net_name:
                            NetID = net_name.index(i.networkname)
                            SearchList.append(net_id[NetID])
                        else:
                            SearchList.append('?') 
                return render(request, 'bulkchange.html', {'changes':PullTest,'search':SearchList})
                    
                
            return render(request, 'bulkchange.html', prompt,{'pull':PullTest})      
    else:
        return redirect('/')
