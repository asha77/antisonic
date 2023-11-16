
def compare_macs(devices, dev_name_1, dev_name_2):
    same_stated_macs = []
    absent_macs = []

    for dev1 in devices:
        if dev1['hostname'] == dev_name_1:
            for dev2 in devices:
                if dev2['hostname'] == dev_name_2:
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
        if dev1['hostname'] == dev_name_2:
            for dev2 in devices:
                if dev2['hostname'] == dev_name_1:
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


def compare_arps(devices, dev_name_1, dev_name_2):
    incompleted_arps = []
    absent_arps = []

    for dev1 in devices:
        if dev1['hostname'] == dev_name_1:
            for dev2 in devices:
                if dev2['hostname'] == dev_name_2:
                    for arp_on_dev1 in dev1['arp_table']:
                        arp_found = False
                        for arp_on_dev2 in dev2['arp_table']:
                            if arp_on_dev1['ip'] == arp_on_dev2['ip']:
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
                                    arp_found = True
                                    break
                        if not arp_found:
                            absent_arps.append([
                                dev1['hostname'],
                                arp_on_dev1['ip'],
                                arp_on_dev1['hwtype'],
                                arp_on_dev1['mac'],
                                arp_on_dev1['flags'],
                                arp_on_dev1['mask'],
                                arp_on_dev1['interface']
                            ])
                    break
            break

    for dev1 in devices:
        if dev1['hostname'] == dev_name_2:
            for dev2 in devices:
                if dev2['hostname'] == dev_name_1:
                    for arp_on_dev1 in dev1['arp_table']:
                        arp_found = False
                        for arp_on_dev2 in dev2['arp_table']:
                            if arp_on_dev1['ip'] == arp_on_dev2['ip']:
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
                                    arp_found = True
                                    break
                        if not arp_found:
                            absent_arps.append([
                                dev1['hostname'],
                                arp_on_dev1['ip'],
                                arp_on_dev1['hwtype'],
                                arp_on_dev1['mac'],
                                arp_on_dev1['flags'],
                                arp_on_dev1['mask'],
                                arp_on_dev1['interface']
                            ])
                    break
            break




    return incompleted_arps, absent_arps