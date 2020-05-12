from django.shortcuts import render, redirect, reverse
import meraki, os, io, csv
from django.contrib import messages
from .models import bulk, subtable, userprofile, vlan, mxport, switch
from django.db.models import Q
import uuid
import datetime
from django.utils import timezone
# Create your views here.

from django.http import HttpResponse
#from django.shortcuts import redirect

def apicheck(request):
    if request.user.is_superuser:
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
        try: 
            apikey = userprofile.objects.get(owner=request.user.id).apikey
        except:
            return redirect('profile')
        my_orgs = ''
        GetOrgList = ''
        table=[]      
        invalidreq=[]
        netcorrect = []
        subs = subtable.objects.filter(Q(owner = request.user.id) & Q(subtype = "addDev") | Q(subtype = "backupDev"))
        # bulk_id=[]
        # bulk_name=[]
        # for i in subs:
            # bulk_id.append(i.id)
            # if i.subtype == "addDev":
                # bulk_name.append("%s-Import-%s"%(i.submissionFname,i.date))
            # else:
                # bulk_name.append("%s-Backup-%s"%(i.submissionFname,i.date))
        substable = SubRefresh(request,filter)
        
        if not apikey == '':
            dashboard = meraki.DashboardAPI(
            api_key = apikey,
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
            orgs = dict(zip(org_name,org_id))                  
            #return render(request, 'bulkchange.html',{'table':table,'bulk_name':bulk_name})
        data = bulk.objects.all()
        prompt = {
            'order': 'The Serial and Network name fields are required. The following fields are supported: Name, Tags, Notes, Address, Static IP, Netmask, Gateway, DNS1, DNS2, VLAN, Network tags.Please note your submission id is auto generated from the csv name',
            'profiles': data
            }
                       
        if 'csvfile' in request.FILES:
            csv_file = request.FILES['csvfile']
            importname = os.path.splitext(csv_file.name)[0]
            subid = uuid.uuid4()
            subtable.objects.update_or_create( 
                id = subid,
                owner = request.user,
                subtype = "addDev",
                submissionFname = importname,
                date = timezone.now()
            )
                    
            
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
                    submissionID = (subtable.objects.get(id=subid)),
                ) 
                   
            context = {}
            return render(request,'bulkchange.html', context ,{'bulk_name':bulk_name,})
        if ('preview' in request.POST) or ('validate' in request.POST) or ('genrevert' in request.POST):
            # try:
                # orgID = request.GET['orgid']
            # except:
                # Error = "Please select a valid Org"
                # return render(request, 'bulkchange.html', {'bulk_name':substable,'orgs':orgs,'error':Error}, prompt)
                
            try:
                submissionID=uuid.UUID(request.POST['sendid'],version=4)
                changes = bulk.objects.filter(submissionID = submissionID)
                operationtype = "selected"
                
            except:
                if not 'genrevert' in request.POST:
                    messages.error(request, "Please select a valid submission ID")
                    return redirect("bulkchange")
                else:
                    operationtype = "all"
                    
            #changes = bulk.objects.filter(submissionID = submissionID)
            try:
                orgID = request.POST['orgid']
            except:
                messages.error(request,"Please select a valid Org")
                return redirect("bulkchange")
            NetID=0      
           
            actions=[]
            
            if not (apikey=='' and orgID==''):
                dashboard = meraki.DashboardAPI(
                api_key = apikey,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
                
                devname = ''
                devserial = ''
                devnetworkID=''
                orgdevserials=[]
                orgdevnetwork=[]
                net_serial=[]
                invalidreq=[]
                netcorrect = []
                networkactions = []
                if 'validate' in request.POST:
                    net_name = []
                    net_id = []
                    new_net_id=[]
                    netcreation=[]
                    
                    my_nets = dashboard.networks.getOrganizationNetworks(orgID)
                    for net in my_nets:
                        net_id.append(net["id"])
                        net_name.append(net["name"])                     
                    for i in changes:
                        if i.networkname in net_name:
                            NetID = net_name.index(i.networkname) 
                            
                        else:                                                        
                            netcreation.append(dashboard.networks.createOrganizationNetwork(orgID,i.networkname,"wireless switch appliance",tags=i.nettags)["id"])
                            
                                
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
                if 'validate' in request.POST:
                    orgdevices=dashboard.organizations.getOrganizationInventory(orgID)
                    for device in orgdevices:
                        orgdevserials.append(device["serial"])
                        orgdevnetwork.append(device["networkId"])
                    net_serial = dict(zip(orgdevserials,orgdevnetwork))
                 
                    for i in changes:
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
                           messages.error(request,"%s is not known in this organisation" % devserial)
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
                        
                if 'genrevert' in request.POST:
                    revertID = request.POST["revertname"]
                    orgdevices=dashboard.organizations.getOrganizationInventory(orgID)
                    for device in orgdevices:
                        orgdevserials.append(device["serial"])
                        orgdevnetwork.append(device["networkId"])
                       
                    net_serial = dict(zip(orgdevserials,orgdevnetwork))
                    subid = uuid.uuid4()
                    subtable.objects.update_or_create( 
                        id = subid,
                        owner = request.user,
                        subtype = "backupDev",
                        submissionFname = revertID,
                        date = timezone.now()
                    )
                    if operationtype == "all":
                        changes = net_serial
                    for i in changes :
                        if operationtype =="all":
                            devserial = i
                        else:
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
                            submissionID = (subtable.objects.get(id=subid))  
                        )
                        
                        #https://pypi.org/project/django-encrypted-model-fields/
                        
            return render(request, 'bulkchange.html', {'pull':changes,'bulk_name':substable,'orgs':orgs})


               
        return render(request, 'bulkchange.html', {'bulk_name':substable,'orgs':orgs}, prompt)      
    else:
        return redirect('/')
def backup(request):
    if request.user.is_authenticated:  
        try: 
            apikey = userprofile.objects.get(owner=request.user.id).apikey
        except:
            return redirect('profile')
        
        filter = subtable.objects.filter(Q(owner = request.user.id) & Q(subtype = "backupOrg"))
              
        substable = SubRefresh(request,filter)
        if not apikey == '':
            dashboard = meraki.DashboardAPI(
            api_key = apikey,
            base_url='https://api-mp.meraki.com/api/v0/',
            log_file_prefix=os.path.basename(__file__)[:-3],
            print_console=False
            )
            my_orgs = dashboard.organizations.getOrganizations()
            org_id = []
            org_name = []
            nets = []
            for org in my_orgs:
                org_id.append(org["id"])
                org_name.append(org["name"])
            orgs = dict(zip(org_name,org_id))
            #orgoID = request.GET['orgoid'] 
            if ('refresh' in request.POST):
                orgoID = request.POST['orgoid']
                if not orgoID in org_id: 
                    messages.error(request,"Error: Refresh requires and org to be selected")
                    return redirect(reverse("backup"))
                my_nets = dashboard.networks.getOrganizationNetworks(orgoID)
                net_id = []
                net_name = []
                for net in my_nets:
                    net_id.append(net["id"])
                    net_name.append(net["name"])
                nets = dict(zip(net_name,net_id)) 
            if ('backup' in request.POST):
                orgoID = request.POST['orgoid']
                #generating the submission
                backupName = request.POST['backupname']
                subid = uuid.uuid4()
                subtable.objects.update_or_create( 
                    id = subid,
                    owner = request.user,
                    subtype = "backupOrg",
                    submissionFname = request.POST['backupname'],
                    date = timezone.now()
                )
                #get the nets and the api calls to get the info we need
                org_nets = dashboard.networks.getOrganizationNetworks(orgoID)               
                net_id = []
                net_name = []
                for net in org_nets:
                    if net['type'] == 'combined':
                        net_id.append(net["id"])
                        net_name.append(net["name"])
                networks = dict(zip(net_name,net_id))
                for i,j in networks.items():
                    try:    
                        devices = dashboard.devices.getNetworkDevices(j)
                        switches=[]
                        for MS in devices:
                            if 'MS' in MS['model']:
                                switches.append(MS['serial'])
                        for serial in switches:
                            netswitch = dashboard.switch_ports.getDeviceSwitchPorts(serial)
                            for ports in netswitch:
                                switch.objects.update_or_create(
                                    submissionID = (subtable.objects.get(id=subid)), 
                                    serial = serial,
                                    netname = i,
                                    number = ports['number'],
                                    enabled = ports['enabled'],
                                    portname = ports['name'],
                                    porttype = ports['type'],
                                    vlan = ports['vlan'],
                                    voicevlan = ports['voiceVlan'],
                                    poe = ports['poeEnabled'],
                                    stp = ports['stpGuard'],
                                    rstp = ports['rstpEnabled'],
                                    )
                    except:
                        messages.error(request,"Unable to backup %s, No valid switches" %i)
                    try:
                        vlans = dashboard.vlans.getNetworkVlans(j)                    
                        for netvlan in vlans:
                            if 'dhcpServerIPs' in netvlan: relayserver = netvlan['dhcpServerIPs']
                            else: relayserver = None
                            vlan.objects.update_or_create(
                                submissionID = (subtable.objects.get(id=subid)),
                                netname = i,
                                vlan = netvlan['id'],
                                vlanname = netvlan['name'],
                                mxip = netvlan['applianceIp'],
                                subnet = netvlan['subnet'],
                                dhcpstatus = netvlan['dhcpHandling'],
                                dhcprelayservers = relayserver,
                                )
                    except:
                         messages.error(request,"Unable to backup %s, No valid vlans" %i)
                    try:    
                        mxports = dashboard.mx_vlan_ports.getNetworkAppliancePorts(j)
                        for ports in mxports:
                            if 'vlan' in ports: mxvlan = ports['vlan']
                            else: mxvlan = None
                            if ports['type'] == 'access':
                                avlans = 'N/A'
                            else:
                                avlan = ports['allowedVlans'] 
                            mxport.objects.update_or_create(
                                submissionID = (subtable.objects.get(id=subid)),
                                netname = i,
                                number = ports['number'],
                                enabled = ports['enabled'],
                                porttype = ports['type'],
                                dropuntag = ports['dropUntaggedTraffic'],
                                vlan = mxvlan,
                                allowedvlans = avlan,
                            )
                    except:
                         messages.error(request,"Unable to backup %s, No valid Mxports" %i)
                messages.success(request,"Backup Complete")         
                return redirect(reverse('backup'))   
                            
            if ('preview' in request.POST):
                try:
                    orgoID = request.POST['orgoid']
                    netlist=[]
                    for i in dashboard.networks.getOrganizationNetworks(orgoID):
                        netlist.append(i["name"])
                except:
                    messages.error(request,"Please Select a Valid Organisation")
                    return redirect(reverse("backup"))
                try:
                    previewID=uuid.UUID(request.POST['backupid'],version=4)
                except ValueError:
                    messages.error(request,"Please Select a Valid Submission")
                    return redirect(reverse("backup"))
               
                if request.POST["netid"] == "All":
                    previewswitch = switch.objects.filter(submissionID = previewID)
                    previewvlan = vlan.objects.filter(submissionID = previewID)
                    previewmxports = mxport.objects.filter(submissionID = previewID)
                elif request.POST["netid"] in netlist:
                    previewnet = request.POST["netid"]
                    previewswitch = switch.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                    previewvlan = vlan.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                    previewmxports = mxport.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                else:
                    messages.error(request,"No matching networks found")
                    return redirect(reverse("backup"))
                return render(request, 'backup.html', {'orgs':orgs, 'backups':substable,'switch':previewswitch,'vlans':previewvlan,'mxports':previewmxports})
            
            if ('restore' in request.POST):
                try:
                    previewID=uuid.UUID(request.POST['backupid'],version=4)
                except ValueError:
                    messages.error(request,"Please Select a valid backup")
                    return redirect(reverse("backup"))
                try:
                    orgoID = request.POST['orgoid']
                    netlist=[]
                   
                except:
                    messages.error(request,"Please Select a Valid Organisation")
                    return redirect(reverse("backup"))
                
                for i in dashboard.networks.getOrganizationNetworks(orgoID):
                    netlist.append(i["name"])
                if request.POST["netid"] == "All":
                    restoreswitch = switch.objects.filter(submissionID = previewID)
                    restorevlan = vlan.objects.filter(submissionID = previewID)
                    restoremxports = mxport.objects.filter(submissionID = previewID)
                elif request.POST["netid"] in netlist:
                    restoreswitch = switch.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                    restorevlan = vlan.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                    restoremxports = mxport.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"]))
                else:
                    messages.error(request,"No matching networks found, please select all at minimum")
                    return redirect(reverse("backup"))
                net_id=[]
                net_name=[]
                my_nets = dashboard.networks.getOrganizationNetworks(orgoID)
                for net in my_nets:
                    net_id.append(net["id"])
                    net_name.append(net["name"])
                restorenetworks = dict(zip(net_name,net_id))
                for serial in restoreswitch:
                    #restorenetID = restorenetworks(serial.netname)
                    dashboard.switch_ports.updateDeviceSwitchPort(serial.serial, serial.number, 
                        name = serial.portname, 
                        enabled = serial.enabled, 
                        type = serial.porttype, 
                        vlan = serial.vlan, 
                        voicevlan = serial.voicevlan, 
                        rstpEnabled = serial.rstp, 
                        stpGuard = serial.stp, 
                        poeEnabled = serial.poe
                        )
                for network in restoremxports:
                    restorenetID = restorenetworks[network.netname]
                    if network.porttype =='trunk':
                        dashboard.mx_vlan_ports.updateNetworkAppliancePort(restorenetID, network.number,
                            enabled = network.enabled,
                            type = network.porttype,
                            vlan = network.vlan,
                            dropUntaggedTraffic = network.dropuntag,
                            allowedVlans = network.allowedvlans,
                            )
                    else: 
                        dashboard.mx_vlan_ports.updateNetworkAppliancePort(restorenetID, network.number,
                            enabled = network.enabled,
                            type = network.porttype,
                            vlan = network.vlan,
                            dropUntaggedTraffic = network.dropuntag,
                            )
                distinctvlans = vlan.objects.filter(Q(submissionID = previewID) & Q(netname = request.POST["netid"])).distinct('netname')
                for i in distinctvlans:
                    restorenetID = restorenetworks[i.netname]
                    if not dashboard.vlans.getNetworkVlansEnabledState(restorenetID): dashboard.vlans.updateVlansEnabledState(restorenetID, True)                    
                    orgvlans = dashboard.vlans.getNetworkVlans(restorenetID)
                    currentVlanList = []
                    for j in orgvlans: currentVlanList.append(orgvlans['id'])
                    restorevlans = vlan.objects.filter(Q(submissionID = previewID) & Q(netname = i.netname))
                    for j in restorevlans:                            
                        if j in currerentVlanLst:
                            if j.dhcpstatus == 'Relay DHCP to another server':
                                dashboard.vlans.updateNetworkVlan(restorenetID, j.vlan,
                                name = j.vlanname,
                                subnet = j.subnet,
                                mxip = j.mxip,
                                dhcpHandling = j.dhcpstatus,
                                dhcpRelayServerIPs = j.dhcprelayservers,   #need to filter this out if handling isn't relay                                      
                                )
                            else:
                                dashboard.vlans.updateNetworkVlan(restorenetID, j.vlan,
                                name = j.vlanname,
                                subnet = j.subnet,
                                mxip = j.mxip,
                                dhcpHandling = j.dhcpstatus
                                )
                        else: 
                            if j.dhcpstatus == 'Relay DHCP to another server':
                                dashboard.createNetworkVlan(restorenetID, j.vlan,
                                j.vlanname,
                                j.subnet,
                                j.mxip,
                                )
                                dashboard.updateNetworkVlan(restorenetID, j.vlan,
                                dhcpHandling = j.dhcpstatus,
                                dhcpRelayServerIPs = j.dhcprelayservers,
                                )
                            else: 
                                dashboard.createNetworkVlan(restorenetID, j.vlan,
                                j.vlanname,
                                j.subnet,
                                j.mxip,
                                )
                                dashboard.updateNetworkVlan(restorenetID, j.vlan,
                                dhcpHandling = j.dhcpstatus,                                
                                )
                messages.success(request,"Restore Complete")
                return redirect(reverse("backup"))
                            
      
                        
        return render(request, 'backup.html', {'orgs':orgs, 'backups':substable,'nets':nets})
    else:
        return redirect('/')
 
def profile(request):
    if request.user.is_authenticated:
        try:
            key = userprofile.objects.get(owner=request.user.id).apikey
            message = "You may change your API Key Below"
        except:
            key = ''
            
            message = "Please Enter your API into the box"
        filter = subtable.objects.filter(owner=request.user.id)  
        substable = SubRefresh(request,filter)
      
            
        if 'key' in request.POST and not request.POST['key']=='':
            try:
                newkey = request.POST['key']
                dashboard = meraki.DashboardAPI(
                api_key = newkey,
                base_url='https://api-mp.meraki.com/api/v0/',
                log_file_prefix=os.path.basename(__file__)[:-3],
                print_console=False
                )
                dashboard.organizations.getOrganizations()
            except:
                message = "Api Key is invalid please try again"
                return render(request, 'profile.html',{'message':message})
            userprofile.objects.get_or_create(owner=request.user) 
            userprofile.objects.update(apikey = newkey)
            key = userprofile.objects.get(owner=request.user.id).apikey
            message = "Key has been update successfuly"
        elif 'key' in request.POST:
            message = "Key length cannot be blank"
            return render(request, 'profile.html',{'message':message})
        #return render(request, 'profile.html',{'message':message, 'currentkey':key,'sub':substable})
       
        if 'Delete' in request.POST:            
            try:
                DelID=uuid.UUID(request.POST['subid'],version=4)
                subtable.objects.get(id = DelID).delete()
                messages.success(request,"Success")
                filter = subtable.objects.filter(owner=request.user.id)  
                substable = SubRefresh(request,filter)
                return redirect(reverse("profile"))
            except ValueError:
                messages.error(request,"Please Select A valid submission")
                return render(request, 'profile.html',{'message':message, 'currentkey':key,'sub':substable})    
        return render(request, 'profile.html',{'message':message, 'currentkey':key,'sub':substable})
    else:
        return redirect('/')
    
def SubRefresh(request,filter):
    try:
       
        sub_id=[]
        sub_name=[]
        for i in filter:
            sub_id.append(i.id)
            if i.subtype == "addDev":
                sub_name.append("%s-ImportedDevices-%s"%(i.submissionFname,i.date))
            elif i.subtype == "backupORG":
                sub_name.append("%s-BackedUpOrganisation-%s"%(i.submissionFname,i.date))
            else:
                sub_name.append("%s-BackedUpDevices-%s"%(i.submissionFname,i.date))
        substable = dict(zip(sub_name,sub_id))        
        return (substable)
    except:
        substable = None
        return (substable)   
        