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
            my_orgs = ''
            GetOrgList = ''
            table=[]      
            invalidreq=[]
            netcorrect = []
            if 'getorg' in request.GET: 
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
                    
                return render(request, 'bulkchange.html',{'table':table})
            data = bulk.objects.all()
            prompt = {
                'order': 'The Serial and Network name fields are required. The following fields are supported: Name, Tags, Notes, Address, Static IP, Netmask, Gateway, DNS1, DNS2, VLAN, Network tags.Please note your submission id is auto generated from the csv name',
                'profiles': data
                }
                           
            if 'csvfile' in request.FILES:
                csv_file = request.FILES['csvfile']
                importname = os.path.splitext(csv_file)[0]
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
                        revert = false,
                        submissionID = importname,
                    ) 
                       
                context = {}
                return render(request,'bulkchange.html', context)
            if ('preview' in request.GET) or ('validate' in request.GET) or ('genrevert' in request.GET):
                changes = bulk.objects.filter(owner=request.user.id)
                api_key = request.GET['apikey']
                orgID = request.GET['orgID']
                NetID=0      
                SearchList=[]
                actions=[]
                
                if not (api_key=='' and orgID==''):
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
                    new_net_id=[]
                    netcreation=[]
                    for org in my_orgs:
                        org_id.append(org["id"])
                        org_name.append(org["name"])
                    my_nets = dashboard.networks.getOrganizationNetworks(orgID)
                    for net in my_nets:
                        net_id.append(net["id"])
                        net_name.append(net["name"])                     
                    for i in changes:
                        if i.networkname in net_name:
                            NetID = net_name.index(i.networkname) 
                            SearchList.append(net_id[NetID])
                        else:
                            if 'validate' in request.GET:
                                SearchList.append("Will be created")
                                netcreation.append(dashboard.networks.createOrganizationNetwork(orgID,i.networkname,"wireless switch appliance",tags=i.nettags)["id"])
                            else:
                                SearchList.append("Needs Creation")
                    devname = ''
                    devserial = ''
                    devnetworkID=''
                    orgdevserials=[]
                    orgdevnetwork=[]
                    net_serial=[]
                    invalidreq=[]
                    netcorrect = []
                    networkactions = []
                    my_nets = dashboard.networks.getOrganizationNetworks(orgID)  #called again to refresh the list with new networks                      
                    for net in my_nets:
                        net_id.append(net["id"])
                        net_name.append(net["name"]) 
                    if 'validate' in request.GET:
                        orgdevices=dashboard.organizations.getOrganizationInventory(orgID)
                        for device in orgdevices:
                            orgdevserials.append(device["serial"])
                            orgdevnetwork.append(device["networkId"])
                        net_serial = dict(zip(orgdevserials,orgdevnetwork))
                        
                        for i in changes:
                            # orgdevices=dashboard.organizations.getOrganizationInventory(orgID)
                            # for device in orgdevices:
                                # orgdevserials.append(device["serial"])
                                # orgdevnetwork.append(device["networkId"])
                            # net_serial = dict(zip(orgdevserials,orgdevnetwork))
                            devname = i.name
                            devserial = i.serial
                            devtags = i.tags
                            devnotes = i.notes
                            devaddress = i.address
                            devip = i.ip
                            devgw = i.gw
                            devmask = i.mask
                            devdns = [i.dns1, i.dns2]
                            devvlan = i.vlan
                            
                            
                            if not i.serial in orgdevserials:
                                invalidreq.append("%s is not known in this organisation" % devserial)
                                continue
                                
                            NetID = net_name.index(i.networkname)
                            destID = net_id[NetID]
                          
                            currentnetworkID = net_serial[devserial]
                            netcorrect.append(currentnetworkID)
                            if currentnetworkID == destID:
                                netcorrect.append("True")
                                #continue # all is fine
                            elif currentnetworkID == None:
                                netcorrect.append("blank")
                                #addactions.append("dashboard.devices.claimNetworkDevices(destID, devserial)")
                                dashboard.devices.claimNetworkDevices(destID, serial = devserial)
                            else: 
                                netcorrect.append("wrong")
                                dashboard.devices.removeNetworkDevice(currentnetworkID, devserial)
                                dashboard.devices.claimNetworkDevices(destID, serial = devserial)
                            if devip == '' and devvlan == '':
                                continue
                            elif devip == "del":
                                wan1 = {"wanEnabled" : "not configured", "usingstaticip" : False}
                            elif devip == '':
                                wan1 = {"wanEnabled" : "not configured", "usingstaticip" : False, "vlan" : devvlan}
                            else :
                                wan1 = {"wanEnabled" : "not configured", "usingstaticip" : True, "staticIp" : devip, "staticGatewayIp" : devgw, "staticSubnetMask" : devmask, "staticDns" : devdns, "vlan" : devvlan}
                                
                            dashboard.management_interface_settings.updateNetworkDeviceManagementInterfaceSettings(destID, devserial,wan1 = wan1)
                            dashboard.devices.updateNetworkDevice(destID, devserial, name = devname, tags = devtags, notes = devnotes)
                            
                    if 'genrevert' in request.GET:
                        revertID = request.GET["revertname"]
                        orgdevices=dashboard.organizations.getOrganizationInventory(orgID)
                        for device in orgdevices:
                            orgdevserials.append(device["serial"])
                            orgdevnetwork.append(device["networkId"])
                           
                        net_serial = dict(zip(orgdevserials,orgdevnetwork))
                       
                        for i in changes :
                            devserial = i.serial
                            currentnetworkID = net_serial[devserial]
                            revertmanagement = (dashboard.management_interface_settings.getNetworkDeviceManagementInterfaceSettings(currentnetworkID, devserial)["wan1"])
                            revertproperties = dashboard.devices.getNetworkDevice(currentnetworkID, devserial)
                            networksets = dashboard.networks.getNetwork(currentnetworkID)
                            if "name" in revertproperties : revname = revertproperties["name"] 
                            else :revname = None
                            if "tags" in revertproperties : revtags = revertproperties["tags"] 
                            else :revtags = None
                            if "notes" in revertproperties : revname = revertproperties["notes"] 
                            else :revnotes = None
                            if "address" in revertproperties : revaddr = revertproperties["address"] 
                            else :revaddr = None
                            if "staticIp" in revertmanagement : 
                                revip = revertmanagement["staticIp"]
                                revgw = revertmanagement["staticGatewayIp"]
                                revmask = revertmanagement["staticSubnetMask"]
                                revdns1 = revertmanagement["staticDns"][0]
                                revdns2 = revertmanagement["staticDns"][1]
                            else :
                                revip = None
                                revgw = None
                                revmask = None
                                revdns1 = None
                                revdns2 = None
                            if "vlan" in revertmanagement : revvlan = revertmanagement["vlan"]
                            else : revvlan = None
                            if "tags" in networksets : revnettags = networksets["tags"]
                            else :revnettags = None                                
                            bulk.objects.update_or_create(
                                serial = devserial,
                                networkname = networksets["name"],
                                name = revname,
                                tags = revtags,
                                notes = revnotes,
                                address = revaddr,
                                ip = revip,
                                gw = revgw,
                                mask = revmask,
                                dns1 = revdns1,
                                dns2 = revdns2,
                                vlan = revvlan,
                                nettags = revnettags,
                                owner = request.user,
                                revert = True,
                                submissionID = revertID 
                            )
                            #revert
                            #https://developer.cisco.com/meraki/api/#/rest/api-endpoints/management-interface-settings/get-network-device-management-interface-settings
                            #https://developer.cisco.com/meraki/api/#/rest/api-endpoints/devices/get-network-device
                            #https://pypi.org/project/django-encrypted-model-fields/
                            
                return render(request, 'bulkchange.html', {'pull':changes,'search':SearchList,'netcr':netcorrect,'invalid':invalidreq})
                    
                
            return render(request, 'bulkchange.html', prompt)      
    else:
        return redirect('/')
