import os.path
import textfsm
import outintofiles
import regparsers


def get_cdp_neighbours_to_model(empty_device, config, curr_path):
    # Extracting for Cisco IOS
    if empty_device['os'] == 'cisco_ios_xe' or empty_device['os'] == 'cisco_ios' or empty_device['os'] == 'cisco_ios_xr':
        nei_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_cdp_nei_ios.template"))

        fsm = textfsm.TextFSM(nei_template)
        fsm.Reset()
        neighbours = fsm.ParseText(config)
        nei_template.close()

        lastindex = 0

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        if len(neighbours) != 0:
            for i in range(lastindex, len(neighbours)):
                if 'N9K' in regparsers.strip_cisco_from_cdp_name(neighbours[i][3]):
                    remote_id = regparsers.strip_serial_from_cdp_name(neighbours[i][1])
                else:
                    remote_id = neighbours[i][1]

                cdp_record = {'local_id': dev_id,
                              'local_model': empty_device['model'],
                              'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                              'local_interface': neighbours[i][4],
                              'remote_id': remote_id,
                              'remote_model': regparsers.strip_cisco_from_cdp_name(neighbours[i][3]),
                              'remote_ip_addr': neighbours[i][2],
                              'remote_interface': neighbours[i][5]
                            }
                empty_device['cdp_neighbours'].append(cdp_record)
        else:
            # let's try lldp neighbours while cdp neighbours not found
            nei_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_lldp_nei_detail.template"))

            fsm = textfsm.TextFSM(nei_template)
            fsm.Reset()
            neighbours_detail = fsm.ParseText(config)
            nei_template.close()


            # let's try lldp neighbours while cdp neighbours not found
            nei_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_lldp_nei.template"))

            fsm = textfsm.TextFSM(nei_template)
            fsm.Reset()
            neighbours = fsm.ParseText(config)
            nei_template.close()

            for i in range(lastindex, len(neighbours_detail)):
                remote_id = neighbours_detail[i][4]

                for j in range(lastindex, len(neighbours)):
                    if neighbours_detail[i][2] == neighbours[j][3]:
                        local_interface = neighbours[j][1]
                        break

                cdp_record = {'local_id': dev_id,
                              'local_model': empty_device['model'],
                              'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                              'local_interface': local_interface,
                              'remote_id': remote_id,
                              'remote_model': neighbours_detail[i][5],
                              'remote_ip_addr': neighbours_detail[i][7],
                              'remote_interface': neighbours_detail[i][2]
                            }
                empty_device['cdp_neighbours'].append(cdp_record)

    # Extracting for Cisco NX-OS
    if empty_device['os'] == 'cisco_nx_os':
        nei_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_cdp_nei_nx_os.template"))
        fsm = textfsm.TextFSM(nei_template)
        fsm.Reset()
        neighbours = fsm.ParseText(config)
        nei_template.close()

        lastindex = 0

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        for i in range(lastindex, len(neighbours)):
            remote_id = regparsers.strip_serial_from_cdp_name(neighbours[i][1])

            if 'N9K' in regparsers.strip_cisco_from_cdp_name(neighbours[i][3]):
                remote_id = regparsers.strip_serial_from_cdp_name(neighbours[i][0])
            else:
                remote_id = neighbours[i][0]

            cdp_record = {'local_id': dev_id,
                          'local_model': empty_device['model'],
                          'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                          'local_interface': neighbours[i][5],
                          'remote_id': remote_id,
                          'remote_model': regparsers.strip_cisco_from_cdp_name(neighbours[i][3]),
                          'remote_ip_addr': neighbours[i][2],
                          'remote_interface': neighbours[i][4]
                          }
            empty_device['cdp_neighbours'].append(cdp_record)

    # Extracting for Huawei
    if empty_device['os'] == 'huawei_vrp':
        nei_template = open(os.path.join(curr_path, 'txtfsm_templates', "huawei", "huawei_lldp_nei.template"))
        fsm = textfsm.TextFSM(nei_template)
        fsm.Reset()
        neighbours = fsm.ParseText(config)
        nei_template.close()

        lastindex = 0

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        for i in range(lastindex, len(neighbours)):
            cdp_record = {'local_id': dev_id,
                          'local_model': empty_device['model'],
                          'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                          'local_interface': neighbours[i][0],
                          'remote_id': neighbours[i][6],
                          'remote_model': regparsers.strip_cisco_from_cdp_name(neighbours[i][3]),
                          'remote_ip_addr': neighbours[i][9],
                          'remote_interface': neighbours[i][4]
                          }
            empty_device['cdp_neighbours'].append(cdp_record)

    # Extracting for HPE Aruba with WC versions of firmware
    if empty_device['os'] == 'aruba_aos-s' and empty_device['sw_version'].find('WC') == 0:
        nei_template = open(os.path.join(curr_path, "txtfsm_templates", "aruba", "lldp_nei_WC.template"))
        fsm = textfsm.TextFSM(nei_template)
        fsm.Reset()
        neighbours = fsm.ParseText(config)
        nei_template.close()

        lastindex = 0

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        for i in range(lastindex, len(neighbours)):
            local_port = neighbours[i][0].strip()
            remote_chassis_id = neighbours[i][1].strip()
            remote_port_id = neighbours[i][2].strip()
            remote_port_desc = neighbours[i][3].strip()
            remote_chassis_name = neighbours[i][4].strip()

            cdp_record = {'local_id': dev_id,
                          'local_model': empty_device['model'],
                          'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                          'local_interface': local_port,
                          'remote_id': remote_chassis_name,
                          'remote_model': '',
                          'remote_ip_addr': '',
                          'remote_interface': remote_port_id
                          }
            empty_device['cdp_neighbours'].append(cdp_record)

    # Extracting for HPE Aruba with YC versions of firmware
    if empty_device['os'] == 'aruba_aos-s' and (empty_device['sw_version'].find('YA') == 0 or empty_device['sw_version'].find('YB') == 0):
        nei_template = open(os.path.join(curr_path, "txtfsm_templates", "aruba", "lldp_nei_YA.template"))
        fsm = textfsm.TextFSM(nei_template)
        fsm.Reset()
        neighbours = fsm.ParseText(config)
        nei_template.close()

        lastindex = 0

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        for i in range(lastindex, len(neighbours)):
            local_port = neighbours[i][0].strip()

            if neighbours[i][1] == '':
                remote_chassis_id = neighbours[i][2].strip()
            else:
                remote_chassis_id = neighbours[i][1].strip()

            if neighbours[i][3] =='':
                if neighbours[i][4] == '':
                    remote_port_id = neighbours[i][5].strip()
                else:
                    remote_port_id = neighbours[i][4].strip()
            else:
                remote_port_id = neighbours[i][3].strip()

            if neighbours[i][6] == '':
                remote_port_desc = neighbours[i][7].strip()
            else:
                remote_port_desc = neighbours[i][6].strip()

            remote_chassis_name = neighbours[i][8].strip()

            cdp_record = {'local_id': dev_id,
                          'local_model': empty_device['model'],
                          'local_ip_addr': empty_device['mgmt_ipv4_from_filename'],
                          'local_interface': local_port,
                          'remote_id': remote_chassis_name,
                          'remote_model': '',
                          'remote_ip_addr': '',
                          'remote_interface': remote_port_id
                          }
            empty_device['cdp_neighbours'].append(cdp_record)

    return empty_device


def get_vrfs(config, curr_path, file, devinfo):
    nei_template = open(os.path.join(curr_path, 'cisco_cdp_nei_ios.template'))
    fsm = textfsm.TextFSM(nei_template)

    fsm.Reset()
    neighbours = fsm.ParseText(config)
    all_neighbours = []
    lastindex = 0
    i = 0

    for i in range(lastindex, len(neighbours)):
        all_neighbours.append([])
        all_neighbours[len(all_neighbours) - 1].append(file)
        all_neighbours[len(all_neighbours) - 1].append(devinfo[0] + '.' + devinfo[2])
        all_neighbours[len(all_neighbours) - 1].append(devinfo[3])
        all_neighbours[len(all_neighbours) - 1].append(devinfo[1])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][4])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][1])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][3])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][2])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][5])
    if i != 0:
        lastindex = i + 1

    nei_template.close()
    return all_neighbours


def get_interfaces_config_to_model(empty_device, config, curr_path):
    if empty_device['os'] == 'cisco_ios_xe' or empty_device['os'] == 'cisco_ios' or empty_device['os'] == 'cisco_ios_xr':
        int_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_interfaces_config.template"))
        fsm = textfsm.TextFSM(int_template)
        fsm.Reset()
        interfaces_config = fsm.ParseText(config)
        int_template.close()

        int_status = get_int_status(config, empty_device['vendor_id'], curr_path)  # TODO: not relevant for routers on IOS!!!

        # 'interface': interf[0]
        # 'name': interf[1]
        # 'status': interf[2]
        # 'vlan': interf[3]
        # 'duplex': interf[4]
        # 'actual_speed': interf[5]
        # 'physical_type': interf[6]

        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        if len(int_status) > 0:
            for intf in interfaces_config:
                trunk_vlan_ids = ''
                if intf[8] != '':
                    trunk_vlan_ids = intf[8]
                if intf[9] != '':
                    trunk_vlan_ids = trunk_vlan_ids + ',' + intf[9]

                for i_key in range(0, len(int_status)):
                    if int_status[i_key]['interface'] == outintofiles.normalize_interface_names(intf[0]):
                        break

                if ((intf[6] == 'access') and (int_status[i_key]['vlan'].isdigit())):
                    swport_mode = 'access'
                    access_vlan = int_status[i_key]['vlan']
                    trunk_vlans = []
                    if intf[16] == 'nonegotiate':
                        dtp_mode = 'nonegotiate'
                    else:
                        dtp_mode = ''
                    interface_status = int_status[i_key]['status']
                elif ((intf[6] == 'trunk') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = ''
                    interface_status = int_status[i_key]['status']
                elif ((intf[6] == 'dynamic auto') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'auto'
                    interface_status = int_status[i_key]['status']
                elif ((intf[6] == 'dynamic desirable') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'desirable'
                    interface_status = int_status[i_key]['status']
                elif ((intf[16] == 'nonegotiate') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'nonegotiate'
                    interface_status = int_status[i_key]['status']
                else:
                    if 'Vlan' in intf[0]:
                        # vlan interface!!!
                        swport_mode = ''     # TODO: check not set = L3 port = no switchport ???
                        access_vlan = ''
                        trunk_vlans = ''
                        dtp_mode = ''
                        interface_status = 'up'
                    else:                    #
                        swport_mode = ''
                        access_vlan = ''
                        trunk_vlans = ''
                        dtp_mode = ''
                        interface_status = 'up'

                interface = {
                    'name': intf[0],
                    'description': intf[1],
                    'type': regparsers.get_interface_type_by_name(intf[0]),  # physical, svi, po, tunnel, loopback, not set
                    'actual_speed': int_status[i_key]['actual_speed'],
                    'physical_type': int_status[i_key]['physical_type'],
                    'ipv4': intf[3],
                    'mgmt': 'no',  # ToDo: add check_management_int() call here
                    'status': interface_status,
                    'vrf': intf[2],
                    'switchport_mode': swport_mode,  # access, trunk
                    'dtp_mode': dtp_mode,
                    'access_vlan': access_vlan,
                    'portfast': intf[20],  # TODO: may be enabled globally
                    'bpduguard': intf[23],  # TODO: may be enabled globally
                    'trunk_vlan_ids': trunk_vlans,
                    'ip_helper': intf[24],
                    'ip_redirects': intf[14],
                    'proxy_arp': intf[15],
                    'native_vlan': intf[10],
                    'voice_vlan': intf[7],
                    'channel_group': intf[11],
                    'channel_group_mode': intf[12],
                    'mdix': intf[21],
                    'dot1x_mab': intf[17],
                    'dot1x_auth_order': intf[13],
                    'dot1x_auth_prio': intf[18],
                    'dot1x_auth_port_control': intf[19]
                }
                empty_device['interfaces'].append(interface)
        else:
            for intf in interfaces_config:
                trunk_vlan_ids = ''
                if intf[8] != '':
                    trunk_vlan_ids = intf[8]
                if intf[9] != '':
                    trunk_vlan_ids = trunk_vlan_ids + ',' + intf[9]

                if intf[6] == 'access':
                    swport_mode = 'access'
                    access_vlan = intf[5]
                    trunk_vlans = []
                    if intf[16] == 'nonegotiate':
                        dtp_mode = 'nonegotiate'
                    else:
                        dtp_mode = ''
                elif intf[6] == 'trunk':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = ''
                elif intf[6] == 'dynamic auto':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'auto'
                elif intf[6] == 'dynamic desirable':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'desirable'
                elif ((intf[16] == 'nonegotiate') and (intf[6] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'nonegotiate'
                else:
                    if 'Vlan' in intf[0]:
                        # vlan interface!!!
                        swport_mode = ''     # TODO: check not set = L3 port = no switchport ???
                        access_vlan = ''
                        trunk_vlans = ''
                        dtp_mode = ''
                    else:                    # all other interfaces
                        swport_mode = ''
                        access_vlan = ''
                        trunk_vlans = ''
                        dtp_mode = ''

                interface = {
                    'name': intf[0],
                    'description': intf[1],
                    'type': regparsers.get_interface_type_by_name(intf[0]),    # physical, svi, po, tunnel, loopback, not set
                    'speed': '',                                        # TODO: may be enabled globally
                    'ipv4': regparsers.ip_mask_to_prefix(intf[3], intf[4]),
                    'mgmt': 'no',                                       # ToDo: add check_management_int() call here
                    'status': 'unknown',
                    'vrf': intf[2],
                    'switchport_mode': swport_mode,                     # access, trunk
                    'dtp_mode': dtp_mode,
                    'access_vlan': access_vlan,
                    'portfast': intf[20],                               # TODO: may be enabled globally
                    'bpduguard': intf[23],                              # TODO: may be enabled globally
                    'trunk_vlan_ids': trunk_vlans,
                    'ip_helper': intf[24],
                    'ip_redirects': intf[14],
                    'proxy_arp': intf[15],
                    'native_vlan': intf[10],
                    'voice_vlan': intf[7],
                    'channel_group': intf[11],
                    'channel_group_mode': intf[12],
                    'mdix': intf[21],
                    'dot1x_mab': intf[17],
                    'dot1x_auth_order': intf[13],
                    'dot1x_auth_prio': intf[18],
                    'dot1x_auth_port_control': intf[19]
                }

                empty_device['interfaces'].append(interface)

    if empty_device['os'] == 'huawei_vrp':
        int_template = open(os.path.join(curr_path, "txtfsm_templates", "huawei", "huawei_interfaces_config.template"))
        fsm = textfsm.TextFSM(int_template)
        fsm.Reset()
        interfaces_config = fsm.ParseText(config)
        int_template.close()

        int_status = get_int_status(config, empty_device['vendor_id'], curr_path)
        if empty_device['domain_name'] == "Not set":
            dev_id = empty_device['hostname']
        else:
            dev_id = empty_device['hostname'] + '.' + empty_device['domain_name']

        if len(int_status) > 0:
            for intf in interfaces_config:
                trunk_vlan_ids = ''
                if intf[8] != '':
                    trunk_vlan_ids = intf[8]
                if intf[9] != '':
                    trunk_vlan_ids = trunk_vlan_ids + ',' + intf[9]

                for i_key in range(0, len(int_status)):
                    if outintofiles.normalize_interface_names(int_status[i_key]['interface']) == outintofiles.normalize_interface_names(intf[0]):
                        break

                if ((intf[6] == 'access') and (int_status[i_key]['vlan'].isdigit())):
                    swport_mode = 'access'
                    access_vlan = int_status[i_key]['vlan']
                    trunk_vlans = []
                    if intf[16] == 'nonegotiate':
                        dtp_mode = 'nonegotiate'
                    else:
                        dtp_mode = ''
                elif ((intf[6] == 'trunk') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = ''
                elif ((intf[6] == 'dynamic auto') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'auto'
                elif ((intf[6] == 'dynamic desirable') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'desirable'
                elif ((intf[16] == 'nonegotiate') and (int_status[i_key]['vlan'] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'nonegotiate'
                else:
                    swport_mode = 'not set'     # TODO: check not set = L3 port = no switchport ???
                    access_vlan = int_status[i_key]['vlan']
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = ''

                interface = {
                    'name': intf[0],
                    'description': intf[1],
                    'type': regparsers.get_interface_type_by_name(intf[0]),  # physical, svi, po, tunnel, loopback, not set
                    'actual_speed': int_status[i_key]['actual_speed'],
                    'physical_type': int_status[i_key]['physical_type'],
                    'ipv4': intf[3],
                    'mgmt': 'no',  # ToDo: add check_management_int() call here
                    'status': int_status[i_key]['status'],
                    'vrf': intf[2],
                    'switchport_mode': swport_mode,  # access, trunk
                    'dtp_mode': dtp_mode,
                    'access_vlan': access_vlan,
                    'portfast': intf[20],  # TODO: may be enabled globally
                    'bpduguard': intf[23],  # TODO: may be enabled globally
                    'trunk_vlan_ids': trunk_vlans,
                    'ip_helper': intf[24],
                    'ip_redirects': intf[14],
                    'proxy_arp': intf[15],
                    'native_vlan': intf[10],
                    'voice_vlan': intf[7],
                    'channel_group': intf[11],
                    'channel_group_mode': intf[12],
                    'mdix': intf[21],
                    'dot1x_mab': intf[17],
                    'dot1x_auth_order': intf[13],
                    'dot1x_auth_prio': intf[18],
                    'dot1x_auth_port_control': intf[19]
                }
                empty_device['interfaces'].append(interface)
        else:
            for intf in interfaces_config:
                trunk_vlan_ids = ''
                if intf[8] != '':
                    trunk_vlan_ids = intf[8]
                if intf[9] != '':
                    trunk_vlan_ids = trunk_vlan_ids + ',' + intf[9]

                if intf[6] == 'access':
                    swport_mode = 'access'
                    access_vlan = intf[5]
                    trunk_vlans = []
                    if intf[16] == 'nonegotiate':
                        dtp_mode = 'nonegotiate'
                    else:
                        dtp_mode = ''
                elif intf[6] == 'trunk':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = ''
                elif intf[6] == 'dynamic auto':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'auto'
                elif intf[6] == 'dynamic desirable':
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'desirable'
                elif ((intf[16] == 'nonegotiate') and (intf[6] == 'trunk')):
                    swport_mode = 'trunk'
                    access_vlan = ''
                    trunk_vlans = regparsers.get_vlan_ids_on_trunk(trunk_vlan_ids)
                    dtp_mode = 'nonegotiate'
                else:
                    swport_mode = 'not set'
                    access_vlan = ''
                    trunk_vlans = ''
                    dtp_mode = ''

                interface = {
                    'name': intf[0],
                    'description': intf[1],
                    'type': regparsers.get_interface_type_by_name(intf[0]),    # physical, svi, po, tunnel, loopback, not set
                    'speed': '',                                        # TODO: may be enabled globally
                    'ipv4': regparsers.ip_mask_to_prefix(intf[3], intf[4]),
                    'mgmt': 'no',                                       # ToDo: add check_management_int() call here
                    'status': 'unknown',
                    'vrf': intf[2],
                    'switchport_mode': swport_mode,                     # access, trunk
                    'dtp_mode': dtp_mode,
                    'access_vlan': access_vlan,
                    'portfast': intf[20],                               # TODO: may be enabled globally
                    'bpduguard': intf[23],                              # TODO: may be enabled globally
                    'trunk_vlan_ids': trunk_vlans,
                    'ip_helper': intf[24],
                    'ip_redirects': intf[14],
                    'proxy_arp': intf[15],
                    'native_vlan': intf[10],
                    'voice_vlan': intf[7],
                    'channel_group': intf[11],
                    'channel_group_mode': intf[12],
                    'mdix': intf[21],
                    'dot1x_mab': intf[17],
                    'dot1x_auth_order': intf[13],
                    'dot1x_auth_prio': intf[18],
                    'dot1x_auth_port_control': intf[19]
                }
                empty_device['interfaces'].append(interface)

    return empty_device


def get_vlans_configuration_to_model(empty_device, config, curr_path):
    # Extract vlan information (id, name) from configuration
    # {'id': '10', 'name': 'users'}

    if empty_device['vendor_id'] == 'cisco':
        vlan_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_vlans_config.template"))
        fsm = textfsm.TextFSM(vlan_template)
        fsm.Reset()
        vlans = fsm.ParseText(config)
        vlan_template.close()

        vlans_configuration = {}

        i: int = 0
        j: int = 0
        w: int = 0

        for i in range(0, len(vlans)):
            if vlans[i][0] != "internal":
                if vlans[i][0].find(',') != -1:
                    vlans_list =vlans[i][0].split(',')
                    for j in range(0, len(vlans_list)):
                        if vlans_list[j].find('-') != -1:
                            inner_list = vlans_list[j].split('-')
                            for k in range(int(inner_list[0]), int(inner_list[1])+1):
                                vlans_configuration[k] = ''
                        else:
                            vlans_configuration[int(vlans_list[j])] = ''
                elif vlans[i][0].find('-') != -1:
                    vlans_list = vlans[i][0].split('-')
                    for j in range(int(vlans_list[0]), int(vlans_list[1])+1):
                        vlans_configuration[j] = ''
                else:
                    try:
                        vlans_configuration[int(vlans[i][0])] = vlans[i][1]
                    except:
                        print("Exception111")

        empty_device['vlans'] = vlans_configuration

    if empty_device['vendor_id'] == 'huawei':
        vlan_template = open(os.path.join(curr_path, "txtfsm_templates", "huawei", "huawei_vlans_config.template"))
        fsm = textfsm.TextFSM(vlan_template)
        fsm.Reset()
        vlans = fsm.ParseText(config)
        vlan_template.close()

        vlans_configuration = {}

        i: int = 0
        j: int = 0
        w: int = 0

        for i in range(0, len(vlans)):
            if vlans[i][0] != "internal":
                if vlans[i][0].find(',') != -1:
                    vlans_list =vlans[i][0].split(',')
                    for j in range(0, len(vlans_list)):
                        if vlans_list[j].find('-') != -1:
                            inner_list = vlans_list[j].split('-')
                            for k in range(int(inner_list[0]), int(inner_list[1])+1):
                                vlans_configuration[k] = ''
                        else:
                            vlans_configuration[int(vlans_list[j])] = ''
                elif vlans[i][0].find('-') != -1:
                    vlans_list = vlans[i][0].split('-')
                    for j in range(int(vlans_list[0]), int(vlans_list[1])+1):
                        vlans_configuration[j] = ''
                else:
                    vlans_configuration[int(vlans[i][0])] = vlans[i][1]
        empty_device['vlans'] = vlans_configuration

    return empty_device


def get_vlan_id_by_name(vlans, id):
    for vlan in vlans:
        if vlan == id:
            return vlans[vlan]
    return ''


def do_vlan_analytics(empty_device):
    """
    fill vlan id for vlans with special names (mentioned in 802.1x policies)
     - users
     - iot_toro
     - media_equip
     - off_equip
     - admin
    """
    vlan_analytics = {}
    vlan_analytics['users'] = get_vlanid_by_name(empty_device['vlans'], 'users')
    vlan_analytics['iot_toro'] = get_vlanid_by_name(empty_device['vlans'], 'iot_toro')
    vlan_analytics['media_equip'] = get_vlanid_by_name(empty_device['vlans'], 'media_equip')
    vlan_analytics['off_equip'] = get_vlanid_by_name(empty_device['vlans'], 'off_equip')
    vlan_analytics['admin'] = get_vlanid_by_name(empty_device['vlans'], 'admin')
    return vlan_analytics


def get_vlanid_by_name(vlans, vlan):
    keys = list(vlans.keys())
    vals = list(vlans.values())
    try:
        ind = vals.index(vlan)
        return keys[ind]
    except ValueError:
        return -1


def get_vlans_from_config(config, curr_path):
    # Extract vlan information (id, name) from configuration
    # {'id': '10', 'name': 'default'}

    vlan_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_vlans_config.template"))
    fsm = textfsm.TextFSM(vlan_template)
    fsm.Reset()
    vlans = fsm.ParseText(config)
    vlan_template.close()

    vlans_configuration = []

    i: int = 0
    j: int = 0
    w: int = 0

    for i in range(0, len(vlans)):
        if vlans[i][0] != "internal":
            if vlans[i][0].find(',') != -1:
                vlans_list =vlans[i][0].split(',')
                for j in range(0, len(vlans_list)):
                    vlan_instance = {
                        'id': vlans_list[j],
                        'name': ''
                    }
                    vlans_configuration.append(vlan_instance)
            else:
                vlan_instance = {
                    'id': vlans[i][0],
                    'name': vlans[i][1]
                }
                vlans_configuration.append(vlan_instance)

    return vlans_configuration


def get_access_config(config, curr_path):
    # Extract vty device access parameters
    access_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_dev_access.template"))
    fsm = textfsm.TextFSM(access_template)
    fsm.Reset()
    access = fsm.ParseText(config)

    access_config = []

    for i in range(0, len(access)):
        access_config.append([])
        access_config[i] = access[i]

    if (len(access) == 0):
        access_config.append([])
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")

        access_config.append([])
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")

    if (len(access) == 1):
        access_config.append([])
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")

    if (access_config[0][0] == ""):
        access_config[0][0] = "Not set"

    if (access_config[0][1] == ""):
        access_config[0][1] = "Not set"

    if (access_config[0][2] == ""):
        access_config[0][2] = "Not set"

    if (access_config[0][3] == ""):
        access_config[0][3] = "Not set"

    if (access_config[0][4] == ""):
        access_config[0][4] = "Not set"

    if (access_config[1][0] == ""):
        access_config[1][0] = "Not set"

    if (access_config[1][1] == ""):
        access_config[1][1] = "Not set"

    if (access_config[1][2] == ""):
        access_config[1][2] = "Not set"

    if (access_config[1][3] == ""):
        access_config[1][3] = "Not set"

    if (access_config[1][4] == ""):
        access_config[1][4] = "Not set"

    access_template.close()
    return access_config


def get_con_access_config(config, curr_path):
    # Extract console device access parameters
    access_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_dev_con_access.template"))
    fsm = textfsm.TextFSM(access_template)
    fsm.Reset()
    access = fsm.ParseText(config)

    access_config = []

    for i in range(0, len(access)):
        access_config.append([])
        access_config[i] = access[i]

    if (len(access) == 0):
        access_config.append([])
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")

    if (access_config[0][0] == ""):
        access_config[0][0] = "Not set"

    if (access_config[0][1] == ""):
        access_config[0][1] = "Not set"

    if (access_config[0][2] == ""):
        access_config[0][2] = "Not set"

    if (access_config[0][3] == ""):
        access_config[0][3] = "Not set"

    if (access_config[0][4] == ""):
        access_config[0][4] = "Not set"

    access_template.close()
    return access_config


def get_tacacs_server_ips(config, curr_path, dev_model):
    '''
    Get tacacs server IPs
    '''

    if ("N9K" in dev_model):
        match = regparsers.re.findall('^tacacs-server\shost\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', config, regparsers.re.MULTILINE)
        if match:
            s = ""
            for i in range(len(match)):
                s = s + " "+match[i]+","
            return s[:-1]
        else:
            return "Fail"
    else:
        # Extract vlan information (id, name) from configuration
        tacacs_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_tacacs_servers.template"))
        fsm = textfsm.TextFSM(tacacs_template)
        fsm.Reset()
        ips = fsm.ParseText(config)
        tacacs_template.close()

        if ips:
            s = ""
            for i in range(len(ips)):
                s = s + " "+ips[i][1]+","
            return s[:-1]
        else:
            match = regparsers.re.findall('^tacacs-server\shost\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', config, regparsers.re.MULTILINE)
            if match:
                s = ""
                for i in range(len(match)):
                    s = s + " " + match[i] + ","
                return s[:-1]
            else:
                return "Fail"


def get_int_status(config, vendor_id, curr_path):
    # Extract interface status from 'show interface status' command output
    if vendor_id == 'cisco':
        int_stat_template = open(os.path.join(curr_path, "txtfsm_templates", "cisco", "cisco_interface_status.template"))
        fsm = textfsm.TextFSM(int_stat_template)
        fsm.Reset()
        int_stat = fsm.ParseText(config)

        interfaces_status = []

        for interf in int_stat:
        # Port      Name     Status     Vlan    Duplex Speed    Type
        # Gi1/0/1           notconnect  1267     auto   auto    10/100/1000BaseTX
        # connected, notconnect, TODO: up (for virtual interfaces)

            if interf[2] == 'connected' or interf[2] == 'up':
                port_status = 'connected'
            elif interf[2] == 'notconnect' or interf[2] == 'down':
                port_status = 'notconnect'
            elif interf[2] == 'disabled':
                port_status = 'notconnect'
            else:
                port_status = 'not_determined'

            interfaces_status.append({
                'interface': interf[0],
                'name': interf[1],
                'status': port_status,
                'vlan': interf[3],
                'duplex': interf[4],
                'actual_speed': interf[5],
                'physical_type': interf[6]
            })

    if vendor_id == 'huawei':
        int_stat_template = open(os.path.join(curr_path, "txtfsm_templates", "huawei", "huawei_interface_description.template"))
        fsm = textfsm.TextFSM(int_stat_template)
        fsm.Reset()
        int_stat = fsm.ParseText(config)

        interfaces_status = []

        for interf in int_stat:
        # Port      Name     Status     Vlan    Duplex Speed    Type
        # Gi1/0/1           notconnect  1267     auto   auto    10/100/1000BaseTX

            if interf[1] == 'connected' or interf[1] == 'up':
                port_status = 'connected'
            if interf[1] == 'notconnect' or interf[1] == 'down':
                port_status = 'notconnect'

            interfaces_status.append({
                'interface': interf[0],
                'name': interf[3],
                'status': port_status,
                'vlan': '0',
                'duplex': '',
                'actual_speed': '',
                'physical_type': ''
            })

    return interfaces_status


def get_macs_to_model(empty_device, config, curr_path):
    if empty_device['os'] == 'sonic_edgecore':
        mac_template = open(os.path.join(curr_path, "txtfsm_templates", "edgecore", "edgecore_show_mac.template"))
        fsm = textfsm.TextFSM(mac_template)
        fsm.Reset()
        macs_parsed = fsm.ParseText(config)

        for mac in macs_parsed:
            empty_device['mac_table'].append({
                'vlan_id': mac[1],
                'mac': mac[2],
                'port': mac[3],
                'ESID': mac[4],
                'DIP': mac[5],
                'state': mac[6]
            })
    return empty_device


def get_arps_to_model(empty_device, config, curr_path):
    # parsing sudo arp -n output

    if empty_device['os'] == 'sonic_edgecore':
        arp_template = open(os.path.join(curr_path, "txtfsm_templates", "edgecore", "edgecore_arp.template"))
        fsm = textfsm.TextFSM(arp_template)
        fsm.Reset()
        arp_parsed = fsm.ParseText(config)

        # if (incomplete) "arp -n" output - arp[2] =='' and we set mac as incomplete
        # TODO: possible to get incomplete from txtfsmparser
        for arp in arp_parsed:
            if arp[2] == '':
                mac = "incomplete"
            else:
                mac = arp[2]

            empty_device['arp_table'].append({
                'ip': arp[0],
                'hwtype': arp[1],
                'mac': mac,
                'flags': arp[3],
                'mask': arp[4],
                'interface': arp[5]
            })
    return empty_device


# TODO: extract only one VTEP (first) VTEP IP - to be done !!!!
def get_esi_to_model(empty_device, config, curr_path):
    if empty_device['os'] == 'sonic_edgecore':
        esi_template = open(os.path.join(curr_path, "txtfsm_templates", "edgecore", "edgecore_vxlan_evpn_ex.template"))
        fsm = textfsm.TextFSM(esi_template)
        fsm.Reset()
        esi_parsed = fsm.ParseText(config)

        for esi in esi_parsed:
            empty_device['esi_table'].append({
                'esi': esi[0],
                'type': esi[1],
                'port': esi[2],
                'status': esi[3],
                'vteps': esi[4],
            })
    return empty_device


# TODO: didnot get ipv6 entries - just ipv4
def get_ip_nei_to_model(empty_device, config, curr_path):
    if empty_device['os'] == 'sonic_edgecore':
        ip_nei_template = open(os.path.join(curr_path, "txtfsm_templates", "edgecore", "edgecode_ip_nei.template"))
        fsm = textfsm.TextFSM(ip_nei_template)
        fsm.Reset()
        ip_nei_parsed = fsm.ParseText(config)

        for ip_nei in ip_nei_parsed:
            empty_device['ip_nei_table'].append({
                'ip': ip_nei[0],
                'dev': ip_nei[1],
                'mac': ip_nei[2],
                'learn': ip_nei[3],
                'used': ip_nei[4],
                'probes': ip_nei[5],
                'state': ip_nei[6],
                'proto': ip_nei[7]
            })

    return empty_device


def get_bgp_routes_to_model(empty_device, config, curr_path):
    if empty_device['os'] == 'sonic_edgecore':
        bgp_routes_template = open(os.path.join(curr_path, "txtfsm_templates", "edgecore", "edgecore_ip_bgp_vrf_all.template"))
        fsm = textfsm.TextFSM(bgp_routes_template)
        fsm.Reset()
        bgp_routes = fsm.ParseText(config)

        # {'vrf': 'default', 'status': 'valid|suppressed|damped|history|best|multipath|internal|RIBFail|Stale|Removed', 'network': '0.0.0.0/0', 'next-hop': '100.64.4.130', 'next-hop-self': 'yes', 'metric': '0', 'local_pref': '50', 'weight': '0', 'as-path': '4292608010 4292608012', 'origin': 'IGP|EGP|incomplete'}
        # 'as-path': '4292608010 4292608012', 'origin': 'IGP|EGP|incomplete'}

        for route in bgp_routes:
            if route[2] == '':
                status = verbose_status(route[1])
            else:
                status = verbose_status(route[1])+','+verbose_status(route[2])

            if route[5] == '<':
                nhs = 'yes'
            else:
                nhs = ''

            if route[10] == 'i':
                org = 'IGP'
            else:
                if route[10] == 'e':
                    org = 'EGP'
                else:
                    if route[10] == '?':
                        org = 'incomplete'
                    else:
                        org = route[10]

            empty_device['bgp_l2vpn_table'].append({
                'vrf': route[0],
                'status': status,
                'network': route[3],
                'nexthop': route[4],
                'next-hop-self': nhs,
                'metric': route[6],
                'local_pref': route[7],
                'weight': route[8],
                'as-path': route[9],
                'origin': org
            })
    return empty_device


def verbose_status(sign):
    # 'status': 'valid|suppressed|damped|history|best|multipath|internal|RIBFail|Stale|Removed'
    if sign == '*':
        return 'valid'
    else:
        if sign == 's':
            return 'suppressed'
        else:
            if sign == 'd':
                return 'damped'
            else:
                if sign == 'h':
                    return 'history'
                else:
                    if sign == '*':
                        return 'best'
                    else:
                        if sign == '=':
                            return 'multipath'
                        else:
                            if sign == 'i':
                                return 'internal'
                            else:
                                if sign == 'r':
                                    return 'RIBFail'
                                else:
                                    if sign == 'S':
                                        return 'Stale'
                                    else:
                                        if sign == 'R':
                                            return 'Removed'
                                        else:
                                            return sign