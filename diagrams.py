import N2G
import regparsers

def get_dev_style_from_model(model):
    new_link_style = "endArrow=classic;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=diamondThin;startFill=1;endFill=0;strokeWidth=5;"
    building_style = "shape=mxgraph.cisco.buildings.generic_building;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    router_style = "shape=mxgraph.cisco.routers.atm_router;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    l2_switch_style = "shape=mxgraph.cisco.switches.workgroup_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    l2_huawei_switch_style = "shape=mxgraph.cisco.switches.workgroup_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#CC6600;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"

    l3_switch_style = "shape=mxgraph.cisco.switches.layer_3_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    l3_huawei_switch_style = "shape=mxgraph.cisco.switches.layer_3_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#CC6600;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"

    nexus_switch_style = "shape=mxgraph.cisco.switches.server_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    ind_switch_style = "shape=mxgraph.cisco.switches.workgroup_switch;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#006600;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
    other_device_style = "rounded=1;whiteSpace=wrap;html=1;"

    # Accton-AS4630-54TE
    # Accton-AS5835-54X
    # Accton-AS7816-64X
    # Accton-AS7726-32X
    # Accton-AS7326-56X


    if ("AS7326-56X" in model):            # LEAF
        return [nexus_switch_style, 120, 60]
    elif ("AS4630" in model):               # OOB Access
        return [l2_switch_style, 120, 60]
    elif ("AS5835" in model):               # OOB Core
        return [l3_switch_style, 120, 120]
    elif ("AS7726-32X" in model):           # BR
        return [router_style, 120, 60]
    elif ("AS7816-64X" in model):           # Spine
        return [ind_switch_style, 120, 60]
    else:
        return [other_device_style, 120, 60]


def shorten_ifname(ifname):
    if ("GigabitEthernet" in ifname):
        return ifname.replace("GigabitEthernet", "ge")
    elif ("TenGigabitEthernet" in ifname):
        return ifname.replace("TenGigabitEthernet", "te")
    elif ("FastEthernet" in ifname):
        return ifname.replace("FastEthernet", "fa")
    elif ("TwentyFiveGigE" in ifname):
        return ifname.replace("TwentyFiveGigE", "tfge")
    else:
        return ifname


def filter_devices(devname):
    if ("wap" in devname):
        return False
    elif "AP-" in devname:      # TODO: custom filter
        return False
    elif "esxi" in devname:      # TODO: custom filter
        return False
    elif "AVX" in devname:      # TODO: custom filter
        return False
    else:
        return True


def get_link_style_from_model(ints):
    # TODO: make more link styles based on actual type of transceivers, not only port type
    # default link style
    new_link_style = "endArrow=none;fillColor=#f8cecc;strokeColor=#FF3399;dashed=1;edgeStyle=entityRelationEdgeStyle;startArrow=none;startFill=0;endFill=0;strokeWidth=5;noEdgeStyle=1;"

    # special link styles
    gig_RJ45_link_style = "endArrow=none;fillColor=#f8cecc;strokeColor=default;startArrow=none;startFill=0;endFill=0;strokeWidth=3;rounded=0;endSize=0;startSize=0;edgeStyle=orthogonalEdgeStyle;"
    ten_gig_link_style = "endArrow=none;fillColor=#f8cecc;strokeColor=#FF0000;startArrow=none;startFill=0;endFill=0;strokeWidth=5;rounded=0;endSize=0;startSize=0;edgeStyle=orthogonalEdgeStyle;"
    twe_gig_fast_link_style = "endArrow=none;fillColor=#f8cecc;strokeColor=#009900;startArrow=none;startFill=0;endFill=0;strokeWidth=7;rounded=0;endSize=0;startSize=0;edgeStyle=orthogonalEdgeStyle;"
    fast_link_style = "endArrow=none;fillColor=#f8cecc;strokeColor=default;startArrow=none;startFill=0;endFill=0;strokeWidth=1;rounded=0;endSize=0;startSize=0;jumpSize=0;edgeStyle=orthogonalEdgeStyle;"

    if ("TenGigabitEthernet" in ints):
        return ten_gig_link_style
    elif ("GigabitEthernet" in ints):
        return gig_RJ45_link_style
    elif ("TwentyFiveGigE" in ints):
        return twe_gig_fast_link_style
    elif ("FastEthernet" in ints):
        return fast_link_style
    else:
        return new_link_style



def trunking_analisys():
    # structure of interfaces
    # dev_id, [
    # INTERFACE [0], DESCRIPTION [1], IP_ADDRESS [2], NETMASK [3], ACCESS_VLAN_ID [4]
    # PORT_MODE [5], VOICE_VLAN_ID [6], TRUNK_VLAN_ID [7], NATIVE_VLAN_ID [8]
    # CHANNEL_GROUP [9], PO_MODE [10], AUTH_MODE [11] ]

    # structure of cdps
    # file [0], src dev_id [1], src model [2], src ip [3], src_port [4],
    # dst dev_id [5], dst model [6], dst IP [7], dst port [8]

    # structure of devices
    # hostname [0], mng_ip [1], domain [2], model [3], serial [4], sw_ver [5]

    for dev in all_devices:
        for link in all_cdps:

            num = 0
            if link[1] == dev[0]:
                num = num + 1
            if num:
                print("Fake")

def create_diagram(devices):
    diagram = N2G.drawio_diagram()
    diagram.add_diagram("Page-1")

# diagram.add_node(id="R2", style=".\\styles\\router.txt")
# diagram.add_node(id="R2", style=router_style)
# diagram.add_node(id="R1", style=router_style)
# diagram.add_node(id="R3", style=router_style)
# diagram.add_link("R1", "R2", src_label="Gi0/1", trgt_label="ge-0/1/2", data={"speed": "1G", "media": "10G-LR"})
# diagram.add_link("R2", "R3", src_label="Gi0/1", trgt_label="ge-0/1/2", data={"speed": "1G", "media": "10G-LR"})

    for device in devices:
        if filter_devices(regparsers.get_only_name(device['hostname'], device['domain_name'])):
            lbtext = regparsers.get_only_name(device['hostname'], device['domain_name']) + "&lt;div&gt;" + device[
                'model'] + "&lt;div&gt;" + device['mgmt_ipv4_from_filename']
            if device['domain_name'] == "Not set":
                dev_id = device['hostname']
            else:
                dev_id = device['hostname'] + "." + device['domain_name']

            style = get_dev_style_from_model(device['model'])
            diagram.add_node(id=dev_id, label=lbtext,
                         style=style[0],
                         width=(style[1]),
                         height=(style[2]),
                         data={"IP": device['mgmt_ipv4_from_filename'], "Serial": device['serial']}
                         )
        else:
            print("skipped: " + device['hostname'])

# Add links between devices on diagram
    for device in devices:
        for cdp_neighbour in device['cdp_neighbours']:
            if filter_devices(regparsers.get_only_name(cdp_neighbour['local_id'], device[
                'domain_name'])) and filter_devices(
                    regparsers.get_only_name(cdp_neighbour['remote_id'], device['domain_name'])):

                linkstyle = get_link_style_from_model(
                    cdp_neighbour['local_interface'])  # ToDo: provide actual data info on links

                diagram.add_link(cdp_neighbour['local_id'], cdp_neighbour['remote_id'],
                             src_label=shorten_ifname(cdp_neighbour['local_interface']),
                             trgt_label=shorten_ifname(cdp_neighbour['remote_interface']),
                             style=linkstyle,
                             data={"speed": "1G", "media": "10G-LR"})
            else:
                print("skipped: " + cdp_neighbour['local_id'] + " - " + cdp_neighbour['remote_id'])

    diagram.layout(algo="drl")
    diagram.dump_file(filename="network_graph.drawio", folder="./output/")
    return
