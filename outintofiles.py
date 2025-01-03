import os
import txtfsmparsers
from datetime import datetime
import regparsers
import json

interfaces = [
    [["Ethernet", "Eth"], "Eth"],
    [["FastEthernet", " FastEthernet", "Fa", "interface FastEthernet"], "Fa"],
    [["GigabitEthernet", "Gi", "GE", " GigabitEthernet", "interface GigabitEthernet"], "Gi"],
    [["TenGigabitEthernet", "Te"], "Te"],
    [["Port-channel", "Po"], "Po"],
    [["Serial"], "Ser"],
    [["Vlan"], "Vlan"],
    [["Loopback"], "Lo"],
    [["Eth-Trunk"], "Eth-Trunk"],
    [["Vlanif"], "Vlanif"],

]


def init_files():
    if not os.path.isdir("output"):
        os.mkdir("output")

    if not os.path.isdir("report"):
        os.mkdir("report")

    # инициализация файла c основным выводом
    resfile = open(os.path.join("output", "cparser_output.csv"), "w")
    resfile.write("Configfile;Hostname;Mng IP from filename;Mng from config;Domain Name;Family;Model;Serial;OS;SW Version;VTP ver.;VTP Mode;VTP Domain;VTP rev.;Ports avail.;Ports used\n")
    resfile.close()

    # инициализация файла с портами, на которых есть соседи
    resfile = open(os.path.join("output", "all_nei_output.csv"), "w")
    resfile.write("Hostname;Source Model;Source Mng IP;Port\n")
    resfile.close()

    # инициализация файла со связями CDP
    resfile = open(os.path.join("output", "cdp_nei_output.csv"), "w")
    resfile.write(
        "ConfigFile;Source hostname;Source Model;Source Mng IP;Source port;Dest hostname;Dest Model;Dest IP;Dest portn\n")
    resfile.close()

    # инициализация файла с перечнем портов, за которыми можно увидеть много MAC-адресов
    resfile = open(os.path.join("output", "many_macs.csv"), "w")
    resfile.write("Hostname;VLAN;MAC;PORT\n")
    resfile.close()

    # инициализация файла с конфигурациями интерфейсов
    resfile = open(os.path.join("output", "interfaces.csv"), "w")
    resfile.write(
        'File Name;Hostname;Domain;Switch type;Num of physical ports;Num of SVI ints;Num of ints w/IP;Num up l3 phys ints;'
        'Num access ints;Num up access ints;Num of trunk interfaces;Num up trunk interf;Num access dot1x ports;'
        'Vlan database;Access Vlans;Trunk Vlans;Proposed vlan list;current native Vlans;current Voice Vlans;'
        'current users vlan id;current iot_toro vlan id;current media_equip vlan id;current off_equip vlan id;'
        'current admin vlan id;'
        '\n')
    resfile.close()

    resfile = open(os.path.join("output", "missed_devices.csv"), "w")
    resfile.write('Hostname;Model;IP;\n')
    resfile.close()

    # initialization of file with all MACs
    resfile = open(os.path.join("output", "all_macs.csv"), "w")
    resfile.write("Hostname;MAC;VLAN;PORT;ESI;DIP;STATE\n")
    resfile.close()

    # initialization of file with all ARPs
    resfile = open(os.path.join("output", "all_arps.csv"), "w")
    resfile.write("Hostname;IP;HWTYPE;MAC;FLAG;MASK;INTERFACE\n")
    resfile.close()

    # инициализация файла c некорректным состоянием MACов
#    resfile = open(os.path.join("output", "same_stated_macs.csv"), "w")
#    resfile.write("Hostname;VLAN;MAC;PORT;ESI;DIP;STATE;Hostname;MAC;VLAN;PORT;ESI;DIP;STATE\n")
#    resfile.close()

    # инициализация файла c отсутствующими МАСами
#    resfile = open(os.path.join("output", "absent_macs.csv"), "w")
#    resfile.write("Hostname;VLAN;MAC;PORT;ESI;DIP;STATE\n")
#    resfile.close()

    # инициализация файла c incomplete статусом ARPов
#    resfile = open(os.path.join("output", "incompleted_arps.csv"), "w")
#    resfile.write("Hostname;IP;HWTYPE;MAC;FLAG;MASR;INTERFACE;Hostname;IP;HWTYPE;MAC;FLAG;MASR;INTERFACE\n")
#    resfile.close()

    # инициализация файла c отсутствующими ARPами
#    resfile = open(os.path.join("output", "absent_arps.csv"), "w")
#    resfile.write("Hostname;IP;HWTYPE;MAC;FLAG;MASR;INTERFACE\n")
#    resfile.close()


def init_comliance_files():
    if not os.path.isdir("output"):
        os.mkdir("output")

    # инициализация файла c основным выводом данных соответствия
    resfile = open(os.path.join("output", "compliance_output.csv"), "w")
    resfile.write("Num;Filename;Hostname;IP;Domain Name;Model;Serial;SW Version;TimeZone;SNMP ver;No SrcRt;"
                  "Pass Encr;Weak Encr;Strong Encr;SSH Chk;Logging buffered (level);SSH Timeout;Boot Cnf;"
                  "ServCnf;CNSCnf;con0 exec-time;con0 trans pref;"
                    "con0 trans inp;con0 logiauth;vty num;vty exec-time;vty trans pref;vty trans inp;"
                    "vty acc class;vty num;vty exec-time;vty trans pref;vty trans inp;vty acc class;syslog TS;"
                    "proxy arp;log con;log sysl;log fail;log succ;tcp-kp-in;tcp-kp-out;"
                    "inetd;bootp;auth_retr;weak_pass;motd;acc_com;acc_conn;"
                    "acc_exec;acc_system;new model;auth_login;auth_enable;ntp srv;BPDU Guard;"
                    "arp inspection;dhcp snoooping;tacacs server ips;disable aux;port security;"
                    "storm control;SNMP usr enc\n")
    resfile.close()


def all_neighbours_file_output(all_neighbours):
    all_found_neighbours = open(os.path.join("output", "all_nei_output.csv"), "a")

    for i in range(len(all_neighbours)):
        all_found_neighbours.write('{0:1s};{1:1s};{2:1s} \n'.format(
            all_neighbours[i][1],
            all_neighbours[i][2],
            all_neighbours[i][3],
            all_neighbours[i][4],
        ))
        all_found_neighbours.write('{0:1s};{1:1s};{2:1s} \n'.format(
            all_neighbours[i][5],
            all_neighbours[i][6],
            all_neighbours[i][7],
            all_neighbours[i][8],
        ))
    all_found_neighbours.close()


def all_neighbours_to_file(devices):
    all_neighbours = open(os.path.join("output", "all_nei_output.csv"), "a", encoding='utf-8')

    for devs in devices:
        for neighbour in devs['cdp_neighbours']:
            all_neighbours.write('{0:1s};{1:1s};{2:1s} \n'.format(
                neighbour['local_id'],
                neighbour['local_model'],
                neighbour['local_ip_addr'],
                neighbour['local_interface']
            ))

            all_neighbours.write('{0:1s};{1:1s};{2:1s} \n'.format(
                neighbour['remote_id'],
                neighbour['remote_model'],
                neighbour['remote_ip_addr'],
                neighbour['remote_interface']
            ))
    all_neighbours.close()
    return True


def connectivity_to_file(devices):
    cdp_neighbours = open(os.path.join("output", "cdp_nei_output.csv"), "a", encoding='utf-8')
#    cdp_neighbours.write("ConfigFile;Source hostname;Source Model;Source Mng IP;Source port;Dest hostname;Dest Model;Dest IP;Dest portn\n")
#   ConfigFile	Source hostname	Source Model	Source Mng IP	Source port	Dest hostname	Dest Model	Dest IP	Dest portn

    for dev in devices:
        for neighbour in dev['cdp_neighbours']:
            cdp_neighbours.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s} \n'.format(
                dev['config_filename'],
                neighbour['local_id'],
                neighbour['local_model'],
                neighbour['local_ip_addr'],
                neighbour['local_interface'],
                neighbour['remote_id'],
                neighbour['remote_model'],
                neighbour['remote_ip_addr'],
                neighbour['remote_interface']
            ))
    cdp_neighbours.close()


def many_macs_file_output(config, curr_path, neighbours, devinfo):
    mac_template = open(os.path.join(curr_path, "cisco_macs.template"))
    mac_fsm = txtfsmparsers.textfsm.TextFSM(mac_template)

    many_macs = open(os.path.join("output", "many_macs.csv"), "a")
#    many_macs.write("Hostname;VLAN;MAC;PORT\n")

    mac_fsm.Reset()
    macs = mac_fsm.ParseText(config)

    if len(macs) !=0:
        multimacs = check_macs(macs, 1)
        for j in range(len(multimacs)):
            nei_found = False
            for k in range(len(neighbours)):
                if normalize_interface_names(multimacs[j][3]) == normalize_interface_names(neighbours[k][4]):
                    nei_found = True
                if not nei_found:
                    many_macs.write('{0:1s};{1:1s};{2:1s};{3:1s} \n'.format(devinfo[0], multimacs[j][2], multimacs[j][0], multimacs[j][3]))
    mac_template.close()
    many_macs.close()


def summary_file_output(devices):
    resfile = open(os.path.join("output", "cparser_output.csv"), "a")
#    resfile.write("Configfile;Hostname;Mng IP;Domain Name;Model;Serial;SW Version;VTP ver.;VTP Mode;VTP Domain;VTP rev.;Ports avail.;Ports used\n")
    # ToDo: сортировать по именам при выводе в файл!!!
    # ToDo: подумать над сравнением двух выводов inventory!!!

    for dev in devices:
        ports_used = 0
        ports_all = 0

        for inter in dev['interfaces']:
            if regparsers.is_physical_interface(inter['type']):
                ports_all = ports_all + 1

                if (inter['status'] == 'connected'):
                    ports_used = ports_used + 1

        # вывод в файл информации по устройстваи и утилизированным портам
        resfile.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s};{9:1s};{10:1s};{11:1s};{12:1s};{13:1s};{14:1d};{15:1d} \n'.format(
            dev['config_filename'],
            dev['hostname'],
            dev['mgmt_ipv4_from_filename'],
            dev['mgmt_v4_autodetect'],
            dev['domain_name'],
            dev['family'],
            dev['model'],
            dev['serial'],
            dev['os'],
            " " +dev['sw_version'],
            dev['vtp_version'],
            dev['vtp_oper_mode'],
            dev['vtp_domain_name'],
            dev['vtp_revision'],
            ports_all,
            ports_used))

    resfile.close()

    return True



def interfaces_to_file(devices):
    f_interfaces = open(os.path.join("output", "interfaces.csv"), "a")

    for dev in devices:
        vlans_all = ""
        ports_used = 0
        ports_all = 0

        for inter in dev['interfaces']:
#            vlans_all = vlans_all + int_config[13][i][1] + " " + int_config[13][i][0]

#            if (i < len(int_config[13])-1):
#                vlans_all = vlans_all + ", "

            # count physical interfaces
            if regparsers.is_physical_interface(inter['type']):
                ports_all = ports_all + 1
                if inter['status'] == 'connected':
                    ports_used = ports_used + 1

        str_vlan_db = '"'
        for key, name in dev['vlans'].items():
            str_vlan_db = str_vlan_db + '{0} {1}, \n'.format(name, key)
        if len(str_vlan_db) > 3:
            str_vlan_db = str_vlan_db[:len(str_vlan_db)-3]
        str_vlan_db = str_vlan_db + '"'


        access_vlans = regparsers.get_access_vlans(dev)
        str_access_vlans = '"'
        for key, name in access_vlans.items():
            str_access_vlans = str_access_vlans + '{0} {1}, \n'.format(name, key)
        if len(str_access_vlans) > 3:
            str_access_vlans = str_access_vlans[:len(str_access_vlans)-3]
        str_access_vlans = str_access_vlans + '"'

        # get dict of specially named vlans with predefined names (802.1x if any)
        # TODO: change txtfsmparsers.do_vlan_analytics() if your vlan names set is different
        vlan_analytics_asis = txtfsmparsers.do_vlan_analytics(dev)

        # propose new ordered set of vlans on device
        native_vlans = regparsers.get_native_vlan_ids(dev['interfaces'])
        if len(native_vlans) == 1:
            vlan_analytics_asis['native'] = int(list(native_vlans)[0])
        elif len(native_vlans) == 0:
            vlan_analytics_asis['native'] = -1
        else:
            vlan_analytics_asis['native'] = int(list(native_vlans)[0])          # TODO: same shit - assertion?

        voice_vlans = regparsers.get_voice_vlan_ids(dev['interfaces'])
        if len(voice_vlans) == 1:
            vlan_analytics_asis['voice'] = int(list(voice_vlans)[0])
        elif len(voice_vlans) == 0:
            vlan_analytics_asis['voice'] = -1
        else:
            vlan_analytics_asis['voice'] = int(list(voice_vlans)[0])          # TODO: same shit - assertion?

        proposed_vlans = proposed_vlans_list(access_vlans)

        str_proposed_vlans = '"'
        for key, name in proposed_vlans.items():
            str_proposed_vlans = str_proposed_vlans + '{0} {1}, \n'.format(name, key)
        if len(str_proposed_vlans) > 3:
            str_proposed_vlans = str_proposed_vlans[:len(str_proposed_vlans)-3]
        str_proposed_vlans = str_proposed_vlans + '"'

        f_interfaces.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1d};{5:1d};{6:1d};{7:1d};{8:1d};{9:1d};{10:1d};{11:1d};{12:1d};{13:1s};{14:1s};{15:1s};{16:1s};{17:1s};{18:1s};{19:1s};{20:1s};{21:1s};{22:1s};{23:1s}\n'.format(
            dev['config_filename'],                                                 # [0] filename
            dev['hostname'],                                                        # [1] hostname
            dev['domain_name'],                                                     # [2] domain name
            '',                                     # TODO: check device type here  # [3] type of switch (asw, dsw, csw, undefined)
            regparsers.get_number_of_physical_ints(dev['interfaces']),              # [4] number of physical interfaces
            regparsers.get_number_of_svis(dev['interfaces']),                       # [5] number of SVI interfaces
            regparsers.get_number_of_ints_with_ip(dev['interfaces']),               # [6] number of interfaces with ip addresses
            regparsers.get_number_of_connected_l3_ints(dev['interfaces']),          # [7] number of connected L3 interfaces
            regparsers.get_number_of_acc_int(dev['interfaces']),                    # [8] number of access interfaces
            regparsers.get_number_of_connected_access_ints(dev['interfaces']),      # [9] number of connected access interfaces
            regparsers.get_number_of_trunk_int(dev['interfaces']),                  # [10] number of trunk interfaces
            regparsers.get_number_of_connected_trunk_ints(dev['interfaces']),       # [11] number of connected trunk interfaces
            regparsers.get_number_of_dot1x_ints(dev['interfaces']),                 # [12] number of access ports with dot1x
            str_vlan_db,                                                            # [13] all vlan from vlan database
            str_access_vlans,                                                       # [14] list of access vlan(s)
            ', '.join(regparsers.get_all_vlan_ids_from_trunk(dev['interfaces'])),   # [15] list of vlan(s) on trunks
            str_proposed_vlans,                                                     # [16] list of proposed vlans to be in database and on trunk
            ', '.join(native_vlans),                                                # [17] list of native vlan(s)
            ', '.join(voice_vlans),                                                 # [18] list of voice vlan(s)
            vlan_id_to_str(vlan_analytics_asis['users']),                           # [19] vlan id of 'users' vlan
            vlan_id_to_str(vlan_analytics_asis['iot_toro']),                        # [20] vlan id of 'iot_toro' vlan
            vlan_id_to_str(vlan_analytics_asis['media_equip']),                     # [21] vlan id of media_equip vlan
            vlan_id_to_str(vlan_analytics_asis['off_equip']),                       # [22] vlan id of off_equip vlan
            vlan_id_to_str(vlan_analytics_asis['admin']),                           # [23] vlan id of admin vlan
        ))

    f_interfaces.close()
    return True


def vlan_id_to_str(id):
    if id == -1:
        return ''
    else:
        return '{0}'.format(id)


def proposed_vlans_list(current_vlans):
    proposed_vlans = {}

    # current = {id: 'name'}

    # TODO: subject to change !!!!
    # куст 007596
    # proposed = {id: 'name'}
    proposed_vlans[1000] = 'native'
    proposed_vlans[254] = 'mgmt'
    proposed_vlans[17] = 'users'
    proposed_vlans[3984] = 'off_equip'
    proposed_vlans[3987] = 'media_equip'

    # dictionary of correct vlan names for proposed list
    nice_dictionary = {150: 'uaz.ent.mgmt.ap_wifi', 8: 'ASUTP_GLZ', 56: 'Pritok', 27: 'ohrana_uaz', 397: 'scada_dop'}

    excluded_keys = [1, 3960, 3986, 13, 3990, -1, 3982]

    for curr_key in list(current_vlans.keys()):
        if curr_key not in list(proposed_vlans.keys()) and curr_key not in excluded_keys:
            if current_vlans[curr_key] == '':
                if curr_key in nice_dictionary.keys():
                    proposed_vlans[curr_key] = nice_dictionary[curr_key]
                else:
                    proposed_vlans[curr_key] = 'not set'
            else:
                if curr_key in nice_dictionary.keys():
                    proposed_vlans[curr_key] = nice_dictionary[curr_key]
                else:
                    proposed_vlans[curr_key] = current_vlans[curr_key]
    return proposed_vlans


# Create a function to easily repeat on many lists:
def ListToFormattedString(alist):
    # Each item is right-adjusted, width=3
    formatted_list = ['{:>3}' for item in alist]
    s = ','.join(formatted_list)
    return s.format(*alist)


def check_macs(macs, count):
    mm_macs = []
    for mac_num in range(len(macs)):
        if macs[mac_num][3] != 'CPU' and ('Po' not in macs[mac_num][3]):
# and macs[mac_num][3] != 'Gi0/1' and ('Po' not in macs[mac_num][3]) and macs[mac_num][3] != 'Gi1/0/1' and ('Twe' not in macs[mac_num][3]) and macs[mac_num][3] != 'Gi0/11'
            if ((len([object() for array in macs if array[3] == macs[mac_num][3]])) > (count -1)):
                mm_macs.append(macs[mac_num])
    return mm_macs


def split_interface(interface):
    num_index = interface.index(next(x for x in interface if x.isdigit()))
    str_part = interface[:num_index]
    num_part = interface[num_index:]
    return [str_part, num_part]


def normalize_interface_names(non_norm_int):
    if non_norm_int == 'Drop':
        return 'Failed'

    tmp = split_interface(non_norm_int)
    interface_type = tmp[0]
    port = tmp[1]
    for int_types in interfaces:
        for names in int_types:
            for name in names:
                if interface_type in name:
                    return_this = int_types[1] + port
                    return return_this
    return 'Failed'


def check_compliance(num, file, curr_path, config, device):
    dev_access = txtfsmparsers.get_access_config(config, curr_path)
    dev_con_access = txtfsmparsers.get_con_access_config(config, curr_path)

    # ToDo: transform to tuple values?
    compliance_result.append([])

    compliance_result[len(compliance_result) - 1] = [
    num,                                # 0
    file,                               # 1
    regparsers.obtain_hostname(config),            # 2
    regparsers.obtain_mng_ip_from_config(device, config),  # 3
    regparsers.obtain_domain(config),              # 4
    regparsers.obtain_model(device['vendor_id'], config),               # 5
    regparsers.obtain_serial(config),              # 6
    " " + regparsers.obtain_software_version(device['os'], config),  # 7
    regparsers.obtain_timezone(config),            # 8
    cisco_security_parsers.obtain_snmp_version(config),        # 9!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cisco_security_parsers.check_source_route(config),         # 10
    cisco_security_parsers.check_service_password_encryption(config), # 11
    cisco_security_parsers.check_weak_enable_password_encryption(config), # 12
    cisco_security_parsers.check_enable_password_encryption_method(config),  # 13
    cisco_security_parsers.check_ssh_version(config),          # 14
    cisco_security_parsers.check_logging_buffered(config),     # 15
    cisco_security_parsers.check_ssh_timeout(config),          # 16
    cisco_security_parsers.check_boot_network(config),         # 17
    cisco_security_parsers.check_service_config(config),       # 18
    cisco_security_parsers.check_cns_config(config),           # 19
    dev_con_access[0][1],               # 20 con0 exec-time
    dev_con_access[0][2],               # 21 con0 transport preferred
    dev_con_access[0][3],               # 22 con0 trans inp
    dev_con_access[0][4],               # 23 con0 logiauth
    dev_access[0][0],                   # 24 vty num
    dev_access[0][1],                   # 25 vty exec-time
    dev_access[0][2],                   # 26 vty trans pref
    dev_access[0][3],                   # 27 vty trans inp
    dev_access[0][4],                   # 28 vty acc class
    dev_access[1][0],                   # 29 vty num
    dev_access[1][1],                   # 30 vty exec-time
    dev_access[1][2],                   # 31 vty trans pref
    dev_access[1][3],                   # 32 vty trans inp
    dev_access[1][4],                   # 33 vty acc class
    cisco_security_parsers.check_syslog_timestamp(config),     # 34
    cisco_security_parsers.check_proxy_arp(config),            # 35
    cisco_security_parsers.check_logging_console(config),      # 36
    cisco_security_parsers.check_logging_syslog(config),       # 37
    cisco_security_parsers.check_log_failures(config),         # 38
    cisco_security_parsers.check_log_success(config),          # 39
    cisco_security_parsers.check_tcp_keepalives_in(config),    # 40
    cisco_security_parsers.check_tcp_keepalives_out(config),   # 41
    cisco_security_parsers.check_inetd_disable(config),        # 42
    cisco_security_parsers.check_bootp_disable(config),        # 43
    cisco_security_parsers.check_authentication_retries(config),   # 44
    cisco_security_parsers.check_weak_local_users_passwords(config), # 45
    cisco_security_parsers.check_motd_banner(config),          # 46
    cisco_security_parsers.check_accounting_commands(config),  # 47
    cisco_security_parsers.check_connection_accounting(config),    # 48
    cisco_security_parsers.check_exec_commands_accounting(config), #49
    cisco_security_parsers.check_system_accounting(config),        # 50
    cisco_security_parsers.check_new_model(config),            # 51
    cisco_security_parsers.check_auth_login(config),           # 52
    cisco_security_parsers.check_auth_enable(config),          # 53
    cisco_security_parsers.get_ntp_servers(config),            # 54
    cisco_security_parsers.check_bpduguard(config),            # 55
    cisco_security_parsers.check_iparp_inspect(config),        # 56
    cisco_security_parsers.check_dhcp_snooping(config),        # 57
    txtfsmparsers.get_tacacs_server_ips(config, curr_path, device['model']),   #58
    cisco_security_parsers.check_aux(config),                  # 59
    cisco_security_parsers.check_portsecurity(config),         # 60
    cisco_security_parsers.check_stormcontrol(config),         # 61
    cisco_security_parsers.obtain_snmp_user_encr(config),      # 62
    cisco_security_parsers.check_snmpv3_authencr(config),      # 63
    cisco_security_parsers.check_snmpv2_ACL(config)            # 64
]


def write_compliance():
    # вывод в файл compliance информации
    resfile = open("output\compliance_output.csv", "a")

    print('| {0:4d} | {1:75s} | {2:25s} | {3:15s} | {4:20s} | {5:18s} | {6:10s} | {7:12s} | {8:12s} | {9:10s} | {10:10s} | {11:10s} | {12:10s} | {13:12s} | {14:6s} | {15:25s} | {16:12s} | {17:6s} | {18:6s} | {19:6s} | {20:14s} | {21:14s} | {22:14s} | {23:12s} | {24:8s} | {25:14s} | {26:14s} | {27:12s} | {28:12s} |{29:8s} | {30:14s} | {31:14s} | {32:12s} | {33:12s} | {34:10s} | {35:10s} | {36:10s} | {37:10s} | {38:10s} | {39:10s} | {40:10s} | {41:10s} | {42:10s} | {43:10s} | {44:10s} | {45:10s} | {46:10s} | {47:10s} | {48:10s} | {49:10s} | {50:10s} | {51:10s} | {52:34s} | {53:34s} | {54:65s} | {55:10s} | {56:10s} | {57:10s} | {58:40s} | {59:10s} | {60:10s} | {61:10s} | {62:10s} | {63:10s} | {64:10s} |'.format(*compliance_result[len(compliance_result) - 1]))
#    resfile.write('{0:4d};{1:75s};{2:25s};{3:15s};{4:20s};{5:18s};{6:10s};{7:12s};{8:12s};{9:10s};{10:10s};{11:10s};{12:10s};{13:12s};{14:6s};{15:25s};{16:12s};{17:6s};{18:6s};{19:6s};{20:14s};{21:14s};{22:14s};{23:12s};{24:8s};{25:14s};{26:14s};{27:12s};{28:12s};{29:8s};{30:14s};{31:14s};{32:12s};{33:12s};{34:10s};{35:10s};{36:10s};{37:10s};{38:10s};{39:10s};{40:10s};{41:10s};{42:10s};{43:10s};{44:10s};{45:10s};{46:10s};{47:10s};{48:10s};{49:10s};{50:10s};{51:10s};{52:29s};{53:30s};{54:65s};{55:10s};{56:10s};{57:10s};{58:40s};{59:10s};{60:10s};{61:10s};{62:10s}\n'.format(*compliance_result[len(compliance_result) - 1]))
    resfile.write('{0:4d};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s};{9:1s};{10:1s};{11:1s};{12:1s};{13:1s};{14:1s};{15:1s};{16:1s};{17:1s};{18:1s};{19:1s};{20:1s};{21:1s};{22:1s};{23:1s};{24:1s};{25:1s};{26:1s};{27:1s};{28:1s};{29:1s};{30:1s};{31:1s};{32:1s};{33:1s};{34:1s};{35:1s};{36:1s};{37:1s};{38:1s};{39:1s};{40:1s};{41:1s};{42:1s};{43:1s};{44:1s};{45:1s};{46:1s};{47:1s};{48:1s};{49:1s};{50:1s};{51:1s};{52:1s};{53:1s};{54:1s};{55:1s};{56:1s};{57:1s};{58:1s};{59:1s};{60:1s};{61:1s};{62:1s};{63:1s};{63:1s}\n'.format(*compliance_result[len(compliance_result) - 1]))
    resfile.close()


def write_xls_report(curr_path, ):
    file_name = os.path.join(curr_path, 'report_templates')
    file_name = os.path.join(file_name, 'compliance_report_template.xlsx')

    compliance_report = load_workbook(filename=file_name)
    sheet_ranges = compliance_report['Compl_report']

    # clearing data if any...
    for row in sheet_ranges['F12:F70']:
        for cell in row:
            cell.value = ""

    sheet_ranges['C3'].value = str(datetime.now())
    # starting to fill in compliance report
    # counting devices without auth on con 0
    i = 0
    for cresult in compliance_result:
        if cresult[23] == "Not set":
            sheet_ranges['F12'].value = sheet_ranges['F12'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F12'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F12'].value

    # counting devices without input acl on vtu 0 4
    i = 0
    for cresult in compliance_result:
        if cresult[28] == "Not set":
            sheet_ranges['F13'].value = sheet_ranges['F13'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F13'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F13'].value

    # counting devices without input acl on vtu 5 15
    i = 0
    for cresult in compliance_result:
        if cresult[33] == "Not set":
            sheet_ranges['F14'].value = sheet_ranges['F14'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F14'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F14'].value

    # counting devices without aaa-new model
    i = 0
    for cresult in compliance_result:
        if cresult[51] == "Not set":
            sheet_ranges['F15'].value = sheet_ranges['F15'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F15'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F15'].value

    # counting devices aaa accounting commands
    i = 0
    for cresult in compliance_result:
        if cresult[47] == "Not set":
            sheet_ranges['F16'].value = sheet_ranges['F16'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F16'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F16'].value

    # counting devices aaa accounting connections
    i = 0
    for cresult in compliance_result:
        if cresult[48] == "Not set":
            sheet_ranges['F17'].value = sheet_ranges['F17'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F17'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F17'].value

    # counting devices aaa accounting exec
    i = 0
    for cresult in compliance_result:
        if cresult[49] == "Not set":
            sheet_ranges['F18'].value = sheet_ranges['F18'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F18'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F18'].value

    # counting devices aaa accounting system
    i = 0
    for cresult in compliance_result:
        if cresult[50] == "Not set":
            sheet_ranges['F19'].value = sheet_ranges['F19'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F19'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F19'].value

    # counting devices aaa authentication login
    i = 0
    for cresult in compliance_result:
        if cresult[52] == "Not set":
            sheet_ranges['F20'].value = sheet_ranges['F20'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F20'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F20'].value

    # counting devices aaa authentication enable
    i = 0
    for cresult in compliance_result:
        if cresult[53] == "Not set":
            sheet_ranges['F21'].value = sheet_ranges['F21'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F21'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F21'].value

    # counting devices with enabled aux
    i = 0
    for cresult in compliance_result:
        if cresult[59] == "Not set":
            sheet_ranges['F22'].value = sheet_ranges['F22'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F22'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F22'].value

    # counting devices with con 0 exec timeout not set
    i = 0
    for cresult in compliance_result:
        if cresult[20] == "Not set":
            sheet_ranges['F23'].value = sheet_ranges['F23'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
        else:
            if int(cresult[20]) > 10:
                sheet_ranges['F23'].value = sheet_ranges['F23'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F23'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F23'].value

    # counting devices with con 0  transport preferred none not set
    i = 0
    for cresult in compliance_result:
        if cresult[21] == "Not set":
            sheet_ranges['F24'].value = sheet_ranges['F24'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F24'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F24'].value

    # counting devices without vty 0 4 transport input ssh
    i = 0
    for cresult in compliance_result:
        if ((cresult[27] == "Not set") or (not cresult[27].find('telnet') == -1)):
            sheet_ranges['F25'].value = sheet_ranges['F25'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F25'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F25'].value

    # counting devices without vty 0 4 exec-timeout 10
    i = 0
    for cresult in compliance_result:
        if cresult[25] == "Not set":
            sheet_ranges['F26'].value = sheet_ranges['F26'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
        else:
            if int(cresult[25]) > 10:
                sheet_ranges['F26'].value = sheet_ranges['F26'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F26'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F26'].value

    # counting devices without vty 0 4 transport preferred none
    i = 0
    for cresult in compliance_result:
        if cresult[26] == "Not set":
            sheet_ranges['F27'].value = sheet_ranges['F27'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F27'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F27'].value

    # counting devices without vty 0 4  ip access-class
    i = 0
    for cresult in compliance_result:
        if cresult[28] == "Not set":
            sheet_ranges['F28'].value = sheet_ranges['F28'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F28'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F28'].value

    # counting devices without vty 5 15 transport input ssh
    i = 0
    for cresult in compliance_result:
        if ((cresult[32] == "Not set") or (not cresult[32].find('telnet') == -1)):
            sheet_ranges['F29'].value = sheet_ranges['F29'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F29'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F29'].value

    # counting devices without vty 5 15 exec-timeout 10
    i = 0
    for cresult in compliance_result:
        if cresult[30] == "Not set":
            sheet_ranges['F30'].value = sheet_ranges['F30'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
        else:
            if int(cresult[30]) > 10:
                sheet_ranges['F30'].value = sheet_ranges['F30'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F30'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F30'].value

    # counting devices without vty 5 15 transport preferred none
    i = 0
    for cresult in compliance_result:
        if cresult[31] == "Not set":
            sheet_ranges['F31'].value = sheet_ranges['F31'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F31'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F31'].value

    # counting devices without vty 5 15 ip access-class
    i = 0
    for cresult in compliance_result:
        if cresult[33] == "Not set":
            sheet_ranges['F32'].value = sheet_ranges['F32'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F32'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F32'].value

    # counting devices without motd
    i = 0
    for cresult in compliance_result:
        if cresult[46] == "Not set":
            sheet_ranges['F33'].value = sheet_ranges['F33'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F33'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F33'].value

    # counting devices without service password-encryption
    i = 0
    for cresult in compliance_result:
        if cresult[11] == "Not set":
            sheet_ranges['F34'].value = sheet_ranges['F34'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F34'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F34'].value

    # counting devices with enable password or weak enable secret encryption
    i = 0
    for cresult in compliance_result:
        if not cresult[12] == "Not set":
            sheet_ranges['F35'].value = sheet_ranges['F35'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
        else:
            if not cresult[13].find('Fail') == -1:
                sheet_ranges['F35'].value = sheet_ranges['F35'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F35'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F35'].value

    # check_service_password_encryption(config),  # 11
    # check_weak_enable_password_encryption(config),  # 12
    # check_enable_password_encryption_method(config),  # 13
    # check_weak_local_users_passwords(config),  # 45

    # counting devices without username <user> secret
    i = 0
    for cresult in compliance_result:
        if (not cresult[45].find('Fail') == -1):
            sheet_ranges['F36'].value = sheet_ranges['F36'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F36'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F36'].value

    # obtain_snmp_version(config),  # 9
    # obtain_snmp_user_encr(config),  # 62
    # check_snmpv3_authencr(config),  # 63
    # check_snmpv2_ACL(config)  # 64

    # counting devices with snmp version 3 without priv

    i = 0
    for cresult in compliance_result:
        if cresult[9] == "v3":
            if not cresult[63] == "priv":
                sheet_ranges['F37'].value = sheet_ranges['F37'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F37'].value = "Настройки SNMPv3 без шифрования найдены на " + str(i) +" устройствах:\n" + sheet_ranges['F37'].value

    # counting devices with correct snmp v2 with ACL
    i = 0
    for cresult in compliance_result:
        if cresult[9] == 'v2c':
            if not cresult[64] == "":
                sheet_ranges['F38'].value = sheet_ranges['F38'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F38'].value = "Настройки SNMPv2 без ACL найдены на " + str(i) +" устройствах:\n" + sheet_ranges['F38'].value

    # counting devices with SNMP v3 users with encryption
    i = 0
    for cresult in compliance_result:
        if cresult[9] == "v3":
            if cresult[62] == "Fail":
                sheet_ranges['F39'].value = sheet_ranges['F39'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
                i = i + 1
    sheet_ranges['F39'].value = "Настройки пользователей SNMPv3 без шифрования найдены на " + str(i) +" устройствах:\n" + sheet_ranges['F39'].value

    # counting devices without domain name
    i = 0
    for cresult in compliance_result:
        if cresult[4] == "Not set":
            sheet_ranges['F40'].value = sheet_ranges['F40'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F40'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F40'].value

    # counting devices without timezone
    i = 0
    for cresult in compliance_result:
        if cresult[8] == "Not set":
            sheet_ranges['F41'].value = sheet_ranges['F41'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F41'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F41'].value

    # counting devices without ssh version 2
    i = 0
    for cresult in compliance_result:
        if cresult[14] == "Not set":
            sheet_ranges['F42'].value = sheet_ranges['F42'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F42'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F42'].value

    # counting devices without ssh timeout
    i = 0
    for cresult in compliance_result:
        if cresult[16] == "Not set":
            sheet_ranges['F43'].value = sheet_ranges['F43'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F43'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F43'].value

    # counting devices without no boot network
    i = 0
    for cresult in compliance_result:
        if cresult[17] == "Not set":
            sheet_ranges['F44'].value = sheet_ranges['F44'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F44'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F44'].value

    # counting devices without no boot network
    i = 0
    for cresult in compliance_result:
        if cresult[18] == "Not set":
            sheet_ranges['F45'].value = sheet_ranges['F45'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F45'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F45'].value

    # counting devices without service tcp-keepalives-in
    i = 0
    for cresult in compliance_result:
        if cresult[40] == "Not set":
            sheet_ranges['F46'].value = sheet_ranges['F46'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F46'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F46'].value

    # counting devices without service tcp-keepalives-out
    i = 0
    for cresult in compliance_result:
        if cresult[41] == "Not set":
            sheet_ranges['F47'].value = sheet_ranges['F47'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F47'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F47'].value

    # counting devices without no ip inetd
    i = 0
    for cresult in compliance_result:
        if cresult[42] == "Not set":
            sheet_ranges['F48'].value = sheet_ranges['F48'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F48'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F48'].value

    # counting devices without no ip bootp server
    i = 0
    for cresult in compliance_result:
        if cresult[43] == "Not set":
            sheet_ranges['F49'].value = sheet_ranges['F49'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F49'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F49'].value

    # counting devices without ip ssh authentication-retries
    i = 0
    for cresult in compliance_result:
        if cresult[44] == "Not set":
            sheet_ranges['F50'].value = sheet_ranges['F50'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F50'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F50'].value

    # counting devices with service pad
    sheet_ranges['F51'].value = "please check pad manually!!! It is for routers mainly!!!"

    # counting devices with cdp
    sheet_ranges['F52'].value = "please check cdp manually!!! Recomendations with caution!!!"

    # counting devices without logging buffered
    i = 0
    for cresult in compliance_result:
        if cresult[15] == "Not set":
            sheet_ranges['F53'].value = sheet_ranges['F53'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F53'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F53'].value

    # counting devices without logging console critical
    i = 0
    for cresult in compliance_result:
        if cresult[36] == "Not set":
            sheet_ranges['F54'].value = sheet_ranges['F54'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F54'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F54'].value

    # counting devices without logging syslog informational
    i = 0
    for cresult in compliance_result:
        if cresult[37] == "Not set":
            sheet_ranges['F55'].value = sheet_ranges['F55'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F55'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F55'].value

    # counting devices without login on-failure log
    i = 0
    for cresult in compliance_result:
        if cresult[38] == "Not set":
            sheet_ranges['F56'].value = sheet_ranges['F56'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F56'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F56'].value

    # counting devices without login on-success log
    i = 0
    for cresult in compliance_result:
        if cresult[39] == "Not set":
            sheet_ranges['F57'].value = sheet_ranges['F57'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F57'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F57'].value

    # counting devices without service timestamps debug datetime
    i = 0
    for cresult in compliance_result:
        if cresult[34] == "Not set":
            sheet_ranges['F58'].value = sheet_ranges['F58'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F58'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F58'].value

    # counting devices without ntp settings
    i = 0
    for cresult in compliance_result:
        if cresult[54] == "Not set":
            sheet_ranges['F59'].value = sheet_ranges['F59'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F59'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F59'].value

    # counting devices without no ip proxy arp
    i = 0
    for cresult in compliance_result:
        if cresult[35] == "Not set":
            sheet_ranges['F60'].value = sheet_ranges['F60'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F60'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F60'].value

    # counting devices with uRPF
    sheet_ranges['F61'].value = "please check uPRPF manually!!! Recomendations with caution!!!"

    # counting devices with OSPF authentification manually
    sheet_ranges['F62'].value = "please check OSPF authentification manually!!! Recomendations with caution!!!"

    # counting devices with BGP authentification manually
    sheet_ranges['F63'].value = "please check BGP authentification manually!!! Recomendations with caution!!!"

    # counting devices with ip source routing enabled
    i = 0
    for cresult in compliance_result:
        if cresult[10] == "Not set":
            sheet_ranges['F64'].value = sheet_ranges['F64'].value + cresult[2] + " " + cresult[3] + " " + cresult[6] + "\n"
            i = i + 1
    sheet_ranges['F64'].value = "Найдено на " + str(i) +" устройствах:\n" + sheet_ranges['F64'].value

    save_workbook(compliance_report, os.path.join("output", "compliance_report.xlsx"))
    compliance_report.close()


def find_missed_devices():
    devs = []
    cdps = []
    missed_devices = []
    dname = ''

    with open(os.path.join("output", "cparser_output.csv"), encoding='utf-8') as f_cparser:
        for line in f_cparser.readlines():
            devs.append(line.split(";"))

    with open(os.path.join("output", "all_nei_output.csv"), encoding='utf-8') as f_allnei:
        for line in f_allnei.readlines():
            cdps.append(line.split(";"))

    for cdp in cdps:
        found = False
        if cdp[0] == "Hostname":
            continue

        for dev in devs:
            if found:
                break

            if dev[0] == "Hostname":
                continue

            if dev[4] == "Not set":
                dname = dev[1]
            else:
                dname = dev[1] + '.' + dev[4]

            if cdp[0] == dname:
                found = True

        if not found:  # cdp entry not found in configurations -> add to missed
            if cdp not in missed_devices:
                missed_devices.append(cdp)
    return missed_devices


def missed_devices_file_output(missed_devices):
    f_missed = open(os.path.join("output", "missed_devices.csv"), "a", encoding='utf-8')
    for i in range(len(missed_devices)):
        f_missed.write('{0:1s};{1:1s};{2:1s}'.format(
            missed_devices[i][0],
            missed_devices[i][1],
            missed_devices[i][2],
        ))
    f_missed.close()


def macs_to_file(devices):
    f_macs = open(os.path.join("output", "all_macs.csv"), "a")
    for dev in devices:
        for mac in dev['mac_table']:
                f_macs.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s}\n'.format(
                    dev['hostname'],
                    mac['mac'],
                    mac['vlan_id'],
                    mac['port'],
                    mac['ESID'],
                    mac['DIP'],
                    mac['state']
                ))
    f_macs.close()


def same_stated_macs_to_file(same_stated_macs, file_suffix):
        f_ss_macs = open(os.path.join("output", "same_stated_macs" + file_suffix + ".csv"), "w")

        for mac in same_stated_macs:
            f_ss_macs.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s};{9:1s};{10:1s};{11:1s};{12:1s};{13:1s}\n'.format(
                mac[0],
                mac[1],
                mac[2],
                mac[3],
                mac[4],
                mac[5],
                mac[6],
                mac[7],
                mac[8],
                mac[9],
                mac[10],
                mac[11],
                mac[12],
                mac[13]
            ))
        f_ss_macs.close()


def absent_macs_to_file(absent_macs, file_suffix):
    f_abs_macs = open(os.path.join("output", "absent_macs" + file_suffix + ".csv"), "w")
    for mac in absent_macs:
        f_abs_macs.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s}\n'.format(
            mac[0],
            mac[1],
            mac[2],
            mac[3],
            mac[4],
            mac[5],
            mac[6],
            mac[7]
        ))
    f_abs_macs.close()


# запись всех ARPов в файл
def arps_to_file(devices):
    f_arps = open(os.path.join("output", "all_arps.csv"), "w")

    for dev in devices:
        for arp in dev['arp_table']:
                f_arps.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s}{6:1s}\n'.format(
                    dev['hostname'],
                    arp['ip'],
                    arp['hwtype'],
                    arp['mac'],
                    arp['flags'],
                    arp['mask'],
                    arp['interface']
                ))
    f_arps.close()


# запись всех ARPов в файл
def ip_neigh_to_file(devices):
    f_ip_nei = open(os.path.join("output", "all_ip_nei.csv"), "w")
    for dev in devices:
        for nei in dev['ip_nei_table']:
                f_ip_nei.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s}{6:1s};{7:1s};{8:1s}\n'.format(
                    dev['hostname'],
                    nei['ip'],
                    nei['dev'],
                    nei['mac'],
                    nei['learn'],
                    nei['used'],
                    nei['probes'],
                    nei['state'],
                    nei['proto']
                ))
    f_ip_nei.close()



def incompleted_arps_to_file(incompleted_arps, file_suffix):
        f_inc_arps = open(os.path.join("output", "incompleted_arps" + file_suffix + ".csv"), "w")

        for arp in incompleted_arps:
            f_inc_arps.write(
                '{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s};{9:1s};{10:1s};{11:1s};{12:1s};{13:1s}\n'.format(
                    arp[0],
                    arp[1],
                    arp[2],
                    arp[3],
                    arp[4],
                    arp[5],
                    arp[6],
                    arp[7],
                    arp[8],
                    arp[9],
                    arp[10],
                    arp[11],
                    arp[12],
                    arp[13]
                ))
        f_inc_arps.close()


def absent_arps_to_file(absent_arps, file_suffix):
    f_abs_arps = open(os.path.join("output", "absent_arps" + file_suffix + ".csv"), "w")
    for arp in absent_arps:
        f_abs_arps.write('{0:1s};{1:1s};{2:1s};{3:1s};{4:1s};{5:1s};{6:1s};{7:1s};{8:1s};{9:1s};{10:1s};{11:1s};{12:1s};{13:1s};{14:1s}\n'.format(
            arp[0],
            arp[1],
            arp[2],
            arp[3],
            arp[4],
            arp[5],
            arp[6],
            arp[7],
            arp[8],
            arp[9],
            arp[10],
            arp[11],
            arp[12],
            arp[13],
            arp[14]
        ))
    f_abs_arps.close()


def sw_stats_to_json(devices):
    sw_stats = {}
    sw_stats['data'] = []

    for dev in devices:
        sw_stats['data'].append({
        '{#SW_HOSTNAME}': dev['hostname'],
        '{#SW_IP}': dev['mgmt_ipv4_from_filename'],
        '{#SW_KNOWN_ERRORS}': dev['known_errors'],
        '{#SW_ALL_ERRORS}': dev['all_errors'],
        '{#ECMP_GROUPS}': dev['ecmp_groups'],
        '{#HOSTS}': dev['hosts'],
        '{#NEXTHOPS}': dev['next_hops']
    })

    with open(os.path.join("output", "switches_inventory.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(sw_stats, ensure_ascii=False, indent=4))


def fab_stats_to_json(stats):
    fab_stats = {}
    fab_stats['data'] = []

    for stat in stats:
        fab_stats['data'].append({

        '{#SW_PAIR}': stat['mh_pair'],
        '{#SAME_STATED_MACS}': stat['same_macs'],
        '{#ABSENT_MACS}': stat['absent_macs'],
        '{#ABSENT_ARPS}': stat['absent_arps'],
        '{#INCOMPLETE_ARPS}': stat['incompleted_arps'],
        '{#INCONSISTANT_ROUTES}': '0'
        })

    with open(os.path.join("output", "switches_analytics.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(fab_stats, ensure_ascii=False, indent=4))


def report_to_file(date, devices, stats):
    pref = devices[0]['hostname'][3:10]

    f_fabric_report = open(os.path.join("report", date + "_" + pref + "_IND_report.txt"), "w", encoding='utf-8')

    f_fabric_report.write('=============== REPORT GENERATED AT {0:25s} ============== \n\n\n'.format(date))
    ind = 1

    f_fabric_report.write('------------------------------------------------------------------------------'
                          '------------------------------------------------------------------------'
                          '----------------------------------------------------------------------------------------\n')

    f_fabric_report.write(
        '| {0:4s} | {1:30s} | {2:20s} | {3:24s} | {4:20s} | {5:45s} | {6:10s} | {7:10s} | {8:12s} | {9:10s} | {10:10s} | {11:10s} | {12:10s} | {13:10s} | {14:10s} | {15:10s} | {16:10s} |\n'.format(
            'Num',
            'hostname',
            'ip address',
            'model',
            'serial',
            'sw version',
            'known errs',
            'all errs',
            'ecmp groups',
            'next hops',
            'hosts',
            'routes',
            'ev_mac_hold',
            'ev_nei_hold',
            'ev_adv_unr',
            'obj-tracks',
            'ipv6_ll'
        ))

    f_fabric_report.write('------------------------------------------------------------------------------'
                          '------------------------------------------------------------------------'
                          '----------------------------------------------------------------------------------------\n')
    for dev in devices:
        f_fabric_report.write('| {0:4d} | {1:30s} | {2:20s} | {3:24s} | {4:20s} | {5:45s} | {6:10s} | {7:10s} | {8:12s} | {9:10s} | {10:10s} | {11:10s} | {12:10s} | {13:10s} | {14:10s} | {15:10s} | {16:10s} |\n'.format(
            ind,
            dev['hostname'],
            dev['mgmt_ipv4_from_filename'],
            dev['model'],
            dev['serial'],
            dev['sw_version'],
            dev['known_errors'],
            dev['all_errors'],
            dev['ecmp_groups'],
            dev['next_hops'],
            dev['hosts'],
            dev['routes'],
            dev['evpn_mh_mac_holdtime'],
            dev['evpn mh neigh-holdtime'],
            dev['evpn_mh_advertise_unreach_neighbor'],
            dev['obj_track_sessions'],
            dev['ipv6_link_local']
        ))
        ind = ind + 1

    f_fabric_report.write('------------------------------------------------------------------------------'
                          '------------------------------------------------------------------------'
                          '------------------------------------------------------------------------\n')

    f_fabric_report.write('\n\n')

    # print errors
    for dev in devices:
        f_fabric_report.write('====================================== ERRORS ON {0:20s} ====================================\n'.format(dev['hostname']))
        for error in dev['errors']:
            f_fabric_report.write('{0:100s}\n'.format(error))

    title = '|       Metric       |'
    same_stated_macs =  '|  Same stated MACs  |'
    absent_macs = '|  Absent MACs       | '
    inc_arps = '|  Incompleted ARPs  |'
    abs_arps = '|  Absent ARPs       |'


    for st in stats:
        title = title + ' {0:3s} |'.format(st['mh_pair'])
        same_stated_macs = same_stated_macs + '    {0:5d}    |'.format(st['same_macs'])
        absent_macs = absent_macs + '    {0:5d}    |'.format(st['absent_macs'])
        inc_arps = inc_arps + '    {0:5d}    |'.format(st['incompleted_arps'])
        abs_arps = abs_arps + '    {0:5d}    |'.format(st['absent_arps'])


    f_fabric_report.write('\n\n')
    f_fabric_report.write('--------------------------------------------------------------------------------\n')
    f_fabric_report.write(title + '\n')
    f_fabric_report.write('--------------------------------------------------------------------------------\n')
    f_fabric_report.write(same_stated_macs + '\n')
    f_fabric_report.write(absent_macs + '\n')
    f_fabric_report.write(inc_arps + '\n')
    f_fabric_report.write(abs_arps + '\n')
    f_fabric_report.write('--------------------------------------------------------------------------------\n')


    f_fabric_report.write('\n\n')
    f_fabric_report.write('=============== Same Stated MACS ======================\n')
    f_fabric_report.write(
        '{0:24s}    {1:6s}    {2:18s}    {3:6s}    {4:30s}    {5:8s}    {6:10s}    {7:24s}    {8:6s}    {9:18s}    {10:6s}    {11:30s}    {12:8s}    {13:10s}\n'.format(
            'hostname 1',
            'VLAN',
            'MAC',
            'Port',
            'ES ID',
            'Dest IP',
            'MAC1 State',
            'hostname 2',
            'VLAN',
            'MAC',
            'Port',
            'ES ID',
            'Dest IP',
            'MAC2 State'
        ))

    for stat in stats:
        for ssmac in stat['ssmacs']:
            f_fabric_report.write('{0:24s}    {1:6s}    {2:18s}    {3:6s}    {4:30s}    {5:8s}    {6:10s}    {7:24s}    {8:6s}    {9:18s}    {10:6s}    {11:30s}    {12:8s}    {13:10s}\n'.format(
                ssmac[0],
                ssmac[1],
                ssmac[2],
                ssmac[3],
                ssmac[4],
                ssmac[5],
                ssmac[6],
                ssmac[7],
                ssmac[8],
                ssmac[9],
                ssmac[10],
                ssmac[11],
                ssmac[12],
                ssmac[13]
            ))

    f_fabric_report.write('\n\n')
    f_fabric_report.write('=============== Absent ARPs ======================\n')

    f_fabric_report.write(
        '{0:24s}    {1:16s}    {2:8s}    {3:18s}    {4:5s}    {5:5s}    {6:8s}    {7:40s}\n'.format(
            'hostname',
            'IP',
            'type',
            'MAC',
            'Flags',
            'Mask',
            'VLAN',
            'State on second switch'
        ))

    for stat in stats:
        for aarp in stat['aarps']:
            f_fabric_report.write(
                '{0:24s}    {1:16s}    {2:8s}    {3:18s}    {4:5s}    {5:5s}    {6:8s}    {7:40s}\n'.format(
                    aarp[0],
                    aarp[1],
                    aarp[2],
                    aarp[3],
                    aarp[4],
                    aarp[5],
                    aarp[6],
                    aarp[7]
                ))

    f_fabric_report.write('\n\n')
    f_fabric_report.write('=============== Incompleted ARPs ======================\n')
    f_fabric_report.write(
        '{0:24s}    {1:15s}    {2:6s}    {3:12s}    {4:5s}    {5:5s}    {6:10s}    {7:24s}    {8:15s}    {9:6s}    {10:12s}    {11:5s}    {12:5s}    {13:10s}\n'.format(
            'Hostname',
            'IP',
            'HWtype',
            'MAC state',
            'Flags',
            'Mask',
            'Interface',
            'Hostname',
            'IP',
            'HWtype',
            'MAC',
            'Flags',
            'Mask',
            'Interface'
        ))

    for stat in stats:
        for iarp in stat['iarps']:
            f_fabric_report.write(
                '{0:24s}    {1:15s}    {2:6s}    {3:12s}    {4:5s}    {5:5s}    {6:10s}    {7:24s}    {8:15s}    {9:6s}    {10:12s}    {11:5s}    {12:5s}    {13:10s}\n'.format(
                    iarp[0],
                    iarp[1],
                    iarp[2],
                    iarp[3],
                    iarp[4],
                    iarp[5],
                    iarp[6],
                    iarp[7],
                    iarp[8],
                    iarp[9],
                    iarp[10],
                    iarp[11],
                    iarp[12],
                    iarp[13]
                ))


    f_fabric_report.write('\n\n')
    f_fabric_report.write('=============== Absent MACs ======================\n')
    f_fabric_report.write(
        '{0:24s}    {1:6s}    {2:20s}    {3:18s}    {4:30s}    {5:15s}    {6:8s}    {7:1s}\n'.format(
            'hostname',
            'vlan_id',
            'mac',
            'port',
            'ES ID',
            'DIP',
            'state',
            'mac type'
        ))


    for stat in stats:
        for amac in stat['amacs']:
            f_fabric_report.write(
                '{0:24s}    {1:6s}    {2:20s}    {3:18s}    {4:30s}    {5:15s}    {6:8s}    {7:1s}\n'.format(
                    amac[0],
                    amac[1],
                    amac[2],
                    amac[3],
                    amac[4],
                    amac[5],
                    amac[6],
                    amac[7]
                ))

    f_fabric_report.close()


def macarpstates_to_file(date, devices, m1dyn_m2stat_a1reach_a2stale, m1dyn_m2stat_a1stale_a2reach, m1stat_m2dyn_a1reach_a2stale, m1stat_m2dyn_a1stale_a2reach, m1dyn_m2stat_a1reach_a2reach, m1stat_m2dyn_a1reach_a2reach, m1stat_m2stat_a1stale_a2stale, record_not_found):
    macs_arp_state_report_report = open(os.path.join("report", date + "_macs_arp_state_report.txt"), "w", encoding='utf-8')

    macs_arp_state_report_report.write('Saving rm1dyn_m2stat_a1reach_a2stale....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1dyn_m2stat_a1reach_a2stale:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))

    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1dyn_m2stat_a1stale_a2reach....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1dyn_m2stat_a1stale_a2reach:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))

    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1stat_m2dyn_a1reach_a2stale....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1stat_m2dyn_a1reach_a2stale:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))

    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1stat_m2dyn_a1stale_a2reach....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1stat_m2dyn_a1stale_a2reach:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))



    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1dyn_m2stat_a1reach_a2reach....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1dyn_m2stat_a1reach_a2reach:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))

    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1stat_m2dyn_a1reach_a2reach....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1stat_m2dyn_a1reach_a2reach:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))


    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('Saving m1stat_m2stat_a1stale_a2stale....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} | {3:30s} | {1:20s} | {4:30s} | {5:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 MAC - state',
            'Dev1 ARP - state',
            'Dev2 hostname',
            'Dev2 MAC - state',
            'Dev2 ARP - state'
        ))

    for record in m1stat_m2stat_a1stale_a2stale:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s}    {3:1s}    {4:1s}    {5:1s}    {6:1s} \n'.format(
                'num',
                record[0],
                record[1]['mac'] + ' - ' + record[1]['state'],
                record[2]['ip'] + ' - ' + record[2]['state'],
                record[3],
                record[4]['mac'] + ' - ' + record[4]['state'],
                record[5]['ip'] + ' - ' + record[5]['state']
                ))



    macs_arp_state_report_report.write('\n\n\n\n')
    macs_arp_state_report_report.write('record_not_found....\n')

    macs_arp_state_report_report.write(
        '| {0:4s} | {1:20s} | {2:30s} |\n'.format(
            'Num',
            'Dev1 hostname',
            'Dev1 ip nei - state',
        ))


    for record in record_not_found:
        macs_arp_state_report_report.write(
            '{0:1s}    {1:1s}    {2:1s} \n'.format(
                'num',
                record[0],
                record[1]['ip'] + ' - ' + record[1]['state']
                ))

    macs_arp_state_report_report.close()