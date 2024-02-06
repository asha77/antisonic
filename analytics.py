
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
                            # TODO: do separate filter function
                            # filter Edgecore MACS and LLD handmade MACs
                            # '14:44:8F' Edgecore
                            # 'D0:77:CE' Edgecore
                            # 'B6:96:91' Intel LLDP
                            # 'E4:9D:73' Edgecore
                            # '32:3E:A7' Intel LLDP
                            # '52:7C:6F' Intel LLDP
                            # '36:73:79' xFusion LLDP
                            # 'E0:01:A6' Edgecore

                            if '14:44:8F' not in mac_on_dev1['mac'] \
                                    and 'D0:77:CE' not in mac_on_dev1['mac'] \
                                    and 'B6:96:91' not in mac_on_dev1['mac'] \
                                    and 'E4:9D:73' not in mac_on_dev1['mac'] \
                                    and '32:3E:A7' not in mac_on_dev1['mac'] \
                                    and '52:7C:6F' not in mac_on_dev1['mac'] \
                                    and '36:73:79' not in mac_on_dev1['mac'] \
                                    and 'E0:01:A6' not in mac_on_dev1['mac']:
                                absent_macs.append([
                                    dev1['hostname'],
                                    mac_on_dev1['vlan_id'],
                                    mac_on_dev1['mac'],
                                    mac_on_dev1['port'],
                                    mac_on_dev1['ESID'],
                                    mac_on_dev1['DIP'],
                                    mac_on_dev1['state']
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
                            # TODO: do separate filter function
                            # filter Edgecore MACS and LLD handmade MACs
                            # '14:44:8F' Edgecore
                            # 'D0:77:CE' Edgecore
                            # 'B6:96:91' Intel LLDP
                            # 'E4:9D:73' Edgecore
                            # '32:3E:A7' Intel LLDP
                            # '52:7C:6F' Intel LLDP
                            # '36:73:79' xFusion LLDP
                            # 'E0:01:A6' Edgecore

                                if '14:44:8F' not in mac_on_dev1['mac'] \
                                    and 'D0:77:CE' not in mac_on_dev1['mac'] \
                                    and 'B6:96:91' not in mac_on_dev1['mac'] \
                                    and 'E4:9D:73' not in mac_on_dev1['mac'] \
                                    and '32:3E:A7' not in mac_on_dev1['mac'] \
                                    and '52:7C:6F' not in mac_on_dev1['mac'] \
                                    and '36:73:79' not in mac_on_dev1['mac'] \
                                    and 'E0:01:A6' not in mac_on_dev1['mac']:

                                    absent_macs.append([
                                    dev1['hostname'],
                                    mac_on_dev1['vlan_id'],
                                    mac_on_dev1['mac'],
                                    mac_on_dev1['port'],
                                    mac_on_dev1['ESID'],
                                    mac_on_dev1['DIP'],
                                    mac_on_dev1['state']
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
