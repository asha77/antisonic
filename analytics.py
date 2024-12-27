from datamodel import mac_types


def compare_macs(devices, dev_name_1, dev_name_2):
    same_stated_macs = []
    absent_macs = []

    for dev1 in devices:
        if dev1['hostname'].upper() == dev_name_1.upper():
            for dev2 in devices:
                if dev2['hostname'].upper() == dev_name_2.upper():
                    mac_found = False
                    for mac_on_dev1 in dev1['mac_table']:
                        for mac_on_dev2 in dev2['mac_table']:
                            if mac_on_dev1['mac'] == mac_on_dev2['mac']:
                                mac_found = True

                                # Check status is not Dynamic / Dynamic on portchannel or on interface
                                if (not mac_on_dev1['port'] == "" and not mac_on_dev2['port'] == ""):
                                    if (not mac_on_dev1['state'] == "Dynamic" and not mac_on_dev2['state'] == "Dynamic"):
                                        if (mac_on_dev1['vlan_id'] == mac_on_dev2['vlan_id']):
                                            same_stated_macs.append([
                                                dev1['hostname'],
                                                mac_on_dev1['vlan_id'],
                                                mac_on_dev1['mac'],
                                                mac_on_dev1['port'],
                                                mac_on_dev1['ESID'],
                                                mac_on_dev1['DIP'],
                                                mac_on_dev1['state'],
                                                dev2['hostname'],
                                                mac_on_dev2['vlan_id'],
                                                mac_on_dev2['mac'],
                                                mac_on_dev2['port'],
                                                mac_on_dev2['ESID'],
                                                mac_on_dev2['DIP'],
                                                mac_on_dev2['state']
                                            ])

                                if ((mac_on_dev1['state'] == "Static" and mac_on_dev2['state'] == "Static")):
                                    if (mac_on_dev1['vlan_id'] == mac_on_dev2['vlan_id']):
                                        for esis in dev1['esi_table']:
                                            if ((mac_on_dev1['ESID'] == esis['esi']) and ("L" in esis['type'])):
                                                same_stated_macs.append([
                                                    dev1['hostname'],
                                                    mac_on_dev1['vlan_id'],
                                                    mac_on_dev1['mac'],
                                                    mac_on_dev1['port'],
                                                    mac_on_dev1['ESID'],
                                                    mac_on_dev1['DIP'],
                                                    mac_on_dev1['state'],
                                                    dev2['hostname'],
                                                    mac_on_dev2['vlan_id'],
                                                    mac_on_dev2['mac'],
                                                    mac_on_dev2['port'],
                                                    mac_on_dev2['ESID'],
                                                    mac_on_dev2['DIP'],
                                                    mac_on_dev2['state']
                                                ])
                        if not mac_found:
                            # filter Edgecore MACS and LLD handmade MACs
                            # '14:44:8F' Edgecore
                            # 'D0:77:CE' Edgecore
                            # 'B6:96:91' Intel LLDP
                            # 'E4:9D:73' Edgecore
                            # '32:3E:A7' Intel LLDP
                            # '52:7C:6F' Intel LLDP
                            # '36:73:79' xFusion LLDP
                            # 'E0:01:A6' Edgecore
#                            mactype = 'other'
                            mactype = mac_types.other

                            if '14:44:8F' in mac_on_dev1['mac'] \
                                    or 'D0:77:CE' in mac_on_dev1['mac'] \
                                    or 'E4:9D:73' in mac_on_dev1['mac'] \
                                    or 'E0:01:A6' in mac_on_dev1['mac'] \
                                    or 'A8:27:C8' in mac_on_dev1['mac'][0:8]:
                                mactype = mac_types.edgecore
                            #                                mactype = 'Edgecore'


                            if 'B6:96:91' not in mac_on_dev1['mac'] \
                                    and '32:3E:A7' not in mac_on_dev1['mac'] \
                                    and '52:7C:6F' not in mac_on_dev1['mac'] \
                                    and '36:73:79' not in mac_on_dev1['mac']:
                                mactype = mac_types.lldp
#                                mactype = 'LLDP'

                            if '100.64.68.' not in mac_on_dev1['DIP'] \
                                    and '100.64.100.' not in mac_on_dev1['DIP'] \
                                    and '100.64.4.' not in mac_on_dev1['DIP'] \
                                    and '100.64.36.' not in mac_on_dev1['DIP'] \
                                    and '100.64.132.' not in mac_on_dev1['DIP']:
                                mactype = mac_types.dip
#                                mactype = 'DIP'


                            absent_macs.append([
                                dev1['hostname'],
                                mac_on_dev1['vlan_id'],
                                mac_on_dev1['mac'],
                                mac_on_dev1['port'],
                                mac_on_dev1['ESID'],
                                mac_on_dev1['DIP'],
                                mac_on_dev1['state'],
                                mactype
                                ])
                    break
            break

    for dev1 in devices:
        if dev1['hostname'].upper() == dev_name_2.upper():
            for dev2 in devices:
                if dev2['hostname'].upper() == dev_name_1.upper():
                    for mac_on_dev1 in dev1['mac_table']:
                        mac_found = False
                        for mac_on_dev2 in dev2['mac_table']:
                            if mac_on_dev1['mac'] == mac_on_dev2['mac']:
                                mac_found = True
                                # Check status is not Dynamic / Dynamic on portchannel or on interface
                                if (not mac_on_dev1['port'] == "" and not mac_on_dev2['port'] == ""):
                                    if (not mac_on_dev1['state'] == "Dynamic" and not mac_on_dev2['state'] == "Dynamic"):
                                        if (mac_on_dev1['vlan_id'] == mac_on_dev2['vlan_id']):
                                            same_stated_macs.append([
                                                dev1['hostname'],
                                                mac_on_dev1['vlan_id'],
                                                mac_on_dev1['mac'],
                                                mac_on_dev1['port'],
                                                mac_on_dev1['ESID'],
                                                mac_on_dev1['DIP'],
                                                mac_on_dev1['state'],
                                                dev2['hostname'],
                                                mac_on_dev2['vlan_id'],
                                                mac_on_dev2['mac'],
                                                mac_on_dev2['port'],
                                                mac_on_dev2['ESID'],
                                                mac_on_dev2['DIP'],
                                                mac_on_dev2['state']
                                            ])
                                            break

                                if ((mac_on_dev1['state'] == "Static" and mac_on_dev2['state'] == "Static")):
                                    if (mac_on_dev1['vlan_id'] == mac_on_dev2['vlan_id']):
                                        for esis in dev1['esi_table']:
                                            if ((mac_on_dev1['ESID'] == esis['esi']) and ("L" in esis['type'])):
                                                same_stated_macs.append([
                                                    dev1['hostname'],
                                                    mac_on_dev1['vlan_id'],
                                                    mac_on_dev1['mac'],
                                                    mac_on_dev1['port'],
                                                    mac_on_dev1['ESID'],
                                                    mac_on_dev1['DIP'],
                                                    mac_on_dev1['state'],
                                                    dev2['hostname'],
                                                    mac_on_dev2['vlan_id'],
                                                    mac_on_dev2['mac'],
                                                    mac_on_dev2['port'],
                                                    mac_on_dev2['ESID'],
                                                    mac_on_dev2['DIP'],
                                                    mac_on_dev2['state']
                                                    ])

                        if not mac_found:
                            # filter Edgecore MACS and LLD handmade MACs
                            # '14:44:8F' Edgecore
                            # 'D0:77:CE' Edgecore
                            # 'A8:27:C8' Edgecore
                            # 'B6:96:91' Intel LLDP
                            # 'E4:9D:73' Edgecore
                            # '32:3E:A7' Intel LLDP
                            # '52:7C:6F' Intel LLDP
                            # '36:73:79' xFusion LLDP
                            # 'E0:01:A6' Edgecore
                            mactype = mac_types.other
#                            mactype = 'other'

                            if '14:44:8F' in mac_on_dev1['mac'][0:8] \
                                    or 'D0:77:CE' in mac_on_dev1['mac'][0:8] \
                                    or 'E4:9D:73' in mac_on_dev1['mac'][0:8] \
                                    or 'E0:01:A6' in mac_on_dev1['mac'][0:8] \
                                    or 'A8:27:C8' in mac_on_dev1['mac'][0:8]:
                                mactype = mac_types.edgecore
                            #                                mactype = 'edgecore'

                            if 'B6:96:91' in mac_on_dev1['mac'][0:8] \
                                    or '32:3E:A7' in mac_on_dev1['mac'][0:8] \
                                    or '52:7C:6F' in mac_on_dev1['mac'][0:8] \
                                    or '36:73:79' in mac_on_dev1['mac'][0:8]:
                                mactype = mac_types.lldp
#                                mactype = 'LLDP'

                            if '100.64.68.' not in mac_on_dev1['DIP'] \
                                    or '100.64.100.' in mac_on_dev1['DIP'] \
                                    or '100.64.4.' in mac_on_dev1['DIP'] \
                                    or '100.64.36.' in mac_on_dev1['DIP'] \
                                    or '100.64.132.' in mac_on_dev1['DIP']:
                                mactype = mac_types.dip
#                                mactype = 'DIP'


                            absent_macs.append([
                                dev1['hostname'],
                                mac_on_dev1['vlan_id'],
                                mac_on_dev1['mac'],
                                mac_on_dev1['port'],
                                mac_on_dev1['ESID'],
                                mac_on_dev1['DIP'],
                                mac_on_dev1['state'],
                                mactype
                            ])
                    break
            break

    return same_stated_macs, absent_macs


def remove_same_mac_dups(ss_macs_input):
    ss_macs_output = []
    dups = []

    for j in range(0, len(ss_macs_input)-1):
        for i in range(0, len(ss_macs_input)-1):
            if ss_macs_input[j][2] == ss_macs_input[i][2] and ss_macs_input[j][1] == ss_macs_input[i][1] and not i == j:
                if not i in dups:
                    dups.append(j)

    for i in range(0, len(ss_macs_input)-1):
        if i not in dups:
            ss_macs_output.append(ss_macs_input[i])
    return ss_macs_output


def remove_absent_mac_dups(absent_macs_input):
    absent_macs_output = []
    dups = []

    for j in range(0, len(absent_macs_input)-1):
        for i in range(0, len(absent_macs_input)-1):
            if absent_macs_input[j][2] == absent_macs_input[i][2] and absent_macs_input[j][1] == absent_macs_input[i][1] and not i == j:
                if not i in dups:
                    dups.append(j)

    for i in range(0, len(absent_macs_input)-1):
        if i not in dups:
            absent_macs_output.append(absent_macs_input[i])
    return absent_macs_output



def remove_dip_lldp_macs(absent_macs_input):
    absent_macs_output = []
    dups = []

    for i in range(0, len(absent_macs_input)-1):
        if absent_macs_input[i][7] == mac_types.lldp or absent_macs_input[i][7] == mac_types.dip:
            continue
        else:
            absent_macs_output.append(absent_macs_input[i])
    return absent_macs_output


def compare_arps(devices, dev_name_1, dev_name_2):
    incompleted_arps = []
    absent_arps = []

    for dev1 in devices:
        if dev1['hostname'].upper() == dev_name_1.upper():
            for dev2 in devices:
                if dev2['hostname'].upper() == dev_name_2.upper():
                    for arp_on_dev1 in dev1['arp_table']:
                        arp_found = False
                        for arp_on_dev2 in dev2['arp_table']:
                            # try to found arp on dev2
                            if arp_on_dev1['ip'] == arp_on_dev2['ip']:
                                # arp on dev2 found!
                                arp_found = True
                                # if arp state is incomplete
                                if (arp_on_dev1['mac'] == "incomplete" or arp_on_dev2['mac'] == "incomplete"):
                                    incompleted_arps.append([
                                        dev1['hostname'],
                                        arp_on_dev1['ip'],
                                        arp_on_dev1['hwtype'],
                                        arp_on_dev1['mac'],
                                        arp_on_dev1['flags'],
                                        arp_on_dev1['mask'],
                                        arp_on_dev1['interface'],
                                        dev2['hostname'],
                                        arp_on_dev2['ip'],
                                        arp_on_dev2['hwtype'],
                                        arp_on_dev2['mac'],
                                        arp_on_dev2['flags'],
                                        arp_on_dev2['mask'],
                                        arp_on_dev2['interface']
                                    ])
                                break

                        # if arp NOT found on second switch in arp table we will search it in 'ip -s nei' table
                        if ((not arp_found) and (not arp_on_dev1['interface'] == 'eth0')):
                            # try to find it in 'ip -s nei' output
                            nei_found = False
                            for ip_nei in dev2['ip_nei_table']:
                                if arp_on_dev1['ip'] == ip_nei['ip']:
                                    nei_found = True
                                    if ip_nei['state'] == 'FAILED' or ip_nei['state'] == 'INCOMPLETE':
                                        absent_arps.append([
                                            dev1['hostname'],
                                            arp_on_dev1['ip'],
                                            arp_on_dev1['hwtype'],
                                            arp_on_dev1['mac'],
                                            arp_on_dev1['flags'],
                                            arp_on_dev1['mask'],
                                            arp_on_dev1['interface'],
                                            ip_nei['ip'],
                                            ip_nei['dev'],
                                            ip_nei['mac'],
                                            ip_nei['learn'],
                                            ip_nei['used'],
                                            ip_nei['probes'],
                                            ip_nei['state'],
                                            ip_nei['proto']
                                            ])

                            if not nei_found:   # not find IP in ARP or even in 'ip -s nei' table -> log it
                                # filter incomplete arps and ARPs on Ethernet (uplinks will have one local ARP record)
                                if ((not arp_on_dev1['mac'] == 'incomplete') and (not 'Ethernet' in arp_on_dev1['interface'])):
                                    absent_arps.append([
                                        dev1['hostname'],
                                        arp_on_dev1['ip'],
                                        arp_on_dev1['hwtype'],
                                        arp_on_dev1['mac'],
                                        arp_on_dev1['flags'],
                                        arp_on_dev1['mask'],
                                        arp_on_dev1['interface'],
                                        'not found in ip -s nei on second switch',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        ''
                                        ])
                    break
            break

    for dev1 in devices:
        if dev1['hostname'].upper() == dev_name_2.upper():
            for dev2 in devices:
                if dev2['hostname'].upper() == dev_name_1.upper():
                    for arp_on_dev1 in dev1['arp_table']:
                        arp_found = False
                        for arp_on_dev2 in dev2['arp_table']:
                            if arp_on_dev1['ip'] == arp_on_dev2['ip']:
                                arp_found = True
                                if ((arp_on_dev1['mac'] == "incomplete" or arp_on_dev2['mac'] == "incomplete") or (arp_on_dev1['mac'] == "incomplete" and arp_on_dev2['mac'] == "incomplete")):
                                    incompleted_arps.append([
                                        dev1['hostname'],
                                        arp_on_dev1['ip'],
                                        arp_on_dev1['hwtype'],
                                        arp_on_dev1['mac'],
                                        arp_on_dev1['flags'],
                                        arp_on_dev1['mask'],
                                        arp_on_dev1['interface'],
                                        dev2['hostname'],
                                        arp_on_dev2['ip'],
                                        arp_on_dev2['hwtype'],
                                        arp_on_dev2['mac'],
                                        arp_on_dev2['flags'],
                                        arp_on_dev2['mask'],
                                        arp_on_dev2['interface']
                                    ])
                                    break

                    # if arp NOT found in arp table will search it in 'ip -s nei' table
                        if ((not arp_found) and (not arp_on_dev1['interface'] == 'eth0')):
                            # try to find it in 'ip -s nei' output
                            nei_found = False
                            for ip_nei in dev2['ip_nei_table']:
                                if arp_on_dev1['ip'] == ip_nei['ip']:
                                    nei_found = True
                                    if ip_nei['state'] == 'FAILED' or ip_nei['state'] == 'INCOMPLETE':
                                        absent_arps.append([
                                            dev1['hostname'],
                                            arp_on_dev1['ip'],
                                            arp_on_dev1['hwtype'],
                                            arp_on_dev1['mac'],
                                            arp_on_dev1['flags'],
                                            arp_on_dev1['mask'],
                                            arp_on_dev1['interface'],
                                            ip_nei['ip'],
                                            ip_nei['dev'],
                                            ip_nei['mac'],
                                            ip_nei['learn'],
                                            ip_nei['used'],
                                            ip_nei['probes'],
                                            ip_nei['state'],
                                            ip_nei['proto']
                                            ])


                            if not nei_found:   # not find IP in ARP or even in 'ip -s nei' table -> log it
                                # filter incomplete arps and ARPs on Ethernet (uplinks will have one local ARP record)
                                if ((not arp_on_dev1['mac'] == 'incomplete') and (not 'Ethernet' in arp_on_dev1['interface'])):
                                    absent_arps.append([
                                        dev1['hostname'],
                                        arp_on_dev1['ip'],
                                        arp_on_dev1['hwtype'],
                                        arp_on_dev1['mac'],
                                        arp_on_dev1['flags'],
                                        arp_on_dev1['mask'],
                                        arp_on_dev1['interface'],
                                        'not found in ip -s nei on second switch',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        ''
                                        ])
                    break
            break

    return incompleted_arps, absent_arps


def check_mac_arps(devices, dev_name_1, dev_name_2):

   m1dyn_m2stat_a1reach_a2stale = []
   m1dyn_m2stat_a1stale_a2reach = []
   m1dyn_m2stat_a1reach_a2reach = []

   m1stat_m2dyn_a1reach_a2stale = []
   m1stat_m2dyn_a1stale_a2reach = []
   m1stat_m2dyn_a1reach_a2reach = []

   m1stat_m2stat_a1stale_a2stale = []


   record_not_found = []

   for dev1 in devices:
       if dev1['hostname'].upper() == dev_name_1.upper():
           for dev2 in devices:
               if dev2['hostname'].upper() == dev_name_2.upper():
                   # try to find same ip in ip neighbours table
                   for ip_nei_on_dev1 in dev1['ip_nei_table']:
                       if ip_nei_on_dev1['state'] == 'NOARP':
                           continue
                       record_found = False
                       for ip_nei_on_dev2 in dev2['ip_nei_table']:
                           if ip_nei_on_dev2['state'] == 'NOARP':
                               continue
                           # try to find same ip neighbour ip on dev2
                           if ip_nei_on_dev1['ip'] == ip_nei_on_dev2['ip']:
                               # try to find same ip in arp tables on dev1 and dev2
                               for arp_on_dev1 in dev1['arp_table']:
                                   if arp_on_dev1['ip'] == ip_nei_on_dev1['ip']:
                                       for arp_on_dev2 in dev2['arp_table']:
                                           if arp_on_dev2['ip'] == ip_nei_on_dev2['ip']:
                                                # IPs found, try to found macs
                                                # try to find MAC states as in arp tables on dev1 and dev2
                                               for mac1 in dev1['mac_table']:
                                                   if mac1['mac'].upper() == arp_on_dev1['mac'].upper():
                                                       for mac2 in dev2['mac_table']:
                                                           if mac2['mac'].upper() == arp_on_dev2['mac'].upper():
                                                               record_found = True
                                                               if mac1['state'].upper() == 'DYNAMIC' and mac2['state'].upper() == 'STATIC' and ip_nei_on_dev1['state'].upper() == 'REACHABLE' and ip_nei_on_dev2['state'].upper() == 'STALE':
                                                                   m1dyn_m2stat_a1reach_a2stale.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True

                                                               if mac1['state'].upper() == 'DYNAMIC' and mac2['state'].upper() == 'STATIC' and ip_nei_on_dev1['state'].upper() == 'STALE' and ip_nei_on_dev2['state'].upper() == 'REACHABLE':
                                                                   m1dyn_m2stat_a1stale_a2reach.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True

                                                               if mac1['state'].upper() == 'STATIC' and mac2['state'].upper() == 'DYNAMIC' and ip_nei_on_dev1['state'].upper() == 'REACHABLE' and ip_nei_on_dev2['state'].upper() == 'STALE':
                                                                   m1stat_m2dyn_a1reach_a2stale.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True

                                                               if mac1['state'].upper() == 'STATIC' and mac2['state'].upper() == 'DYNAMIC' and ip_nei_on_dev1['state'].upper() == 'STALE' and ip_nei_on_dev2['state'].upper() == 'REACHABLE':
                                                                   m1stat_m2dyn_a1stale_a2reach.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True

                                                               if mac1['state'].upper() == 'DYNAMIC' and mac2['state'].upper() == 'STATIC' and ip_nei_on_dev1['state'].upper() == 'REACHABLE' and ip_nei_on_dev2['state'].upper() == 'REACHABLE':
                                                                   m1dyn_m2stat_a1reach_a2reach.append([
                                                                           dev1['hostname'],
                                                                           mac1,
                                                                           ip_nei_on_dev1,
                                                                           dev2['hostname'],
                                                                           mac2,
                                                                           ip_nei_on_dev2
                                                                       ])
                                                                   record_found = True

                                                               if mac1['state'].upper() == 'STATIC' and mac2['state'].upper() == 'DYNAMIC' and ip_nei_on_dev1['state'].upper() == 'REACHABLE' and ip_nei_on_dev2['state'].upper() == 'REACHABLE':
                                                                   m1stat_m2dyn_a1reach_a2reach.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True


                                                               if mac1['state'].upper() == 'STATIC' and mac2['state'].upper() == 'STATIC' and ip_nei_on_dev1['state'].upper() == 'STALE' and ip_nei_on_dev2['state'].upper() == 'STALE':
                                                                   m1stat_m2stat_a1stale_a2stale.append([
                                                                       dev1['hostname'],
                                                                       mac1,
                                                                       ip_nei_on_dev1,
                                                                       dev2['hostname'],
                                                                       mac2,
                                                                       ip_nei_on_dev2
                                                                   ])
                                                                   record_found = True
                       # if all records not found add it here
                       if not record_found:
                           record_not_found.append([
                               dev1['hostname'],
                               ip_nei_on_dev1
                           ])

   return m1dyn_m2stat_a1reach_a2stale, m1dyn_m2stat_a1stale_a2reach, m1stat_m2dyn_a1reach_a2stale, m1stat_m2dyn_a1stale_a2reach, m1dyn_m2stat_a1reach_a2reach, m1stat_m2dyn_a1reach_a2reach, m1stat_m2stat_a1stale_a2stale, record_not_found



def get_all_routes(devices):
    all_routes = []
    for dev in devices:
        if dev['hostname'].upper():
            return all_routes

    return all_routes