import argparse
import out_to_screen
import outintofiles
import check_duplicates
import txtfsmparsers
import datamodel
import os
import pathlib
import regparsers
import analytics
import copy
from alive_progress import alive_bar
from datetime import datetime

compliance_result = []
devices = []
empty_device = {}


def createparser():
    parser = argparse.ArgumentParser(prog='CiscoParser', description='Utility for analyzing network device configurations v0.6.', epilog='author: asha77@gmail.com')
    parser.add_argument('-d', '--configdir', required=False, help='Specify directory with cisco config files', type=pathlib.Path)
    parser.add_argument('-c', '--compcheck', required=False, help='Perform compliance check on config files', action='store_true')
    parser.add_argument('-u', '--disablefilecheck', required=False, help='Disable checking for unique devices config files', action='store_true')
    parser.add_argument('-e', '--extractdata', required=False, help='Perform extraction of data from configs and diagnostic commands and draw picture', action='store_true')
    return parser


def main():
    mh_pairs_stats = {}
    stats = []

    parser = createparser()
    namespace = parser.parse_args()

    curr_path = os.path.abspath(os.getcwd())
    if namespace.configdir:
        os.chdir(namespace.configdir)

    if namespace.extractdata is True:
        # get list of files with configs and diagnostic
        list_of_files = os.listdir(namespace.configdir)
        print("Starting processing files in folder: " + str(namespace.configdir))

        # create output files where we will save results
        outintofiles.init_files()

        # check file duplicates using extracted serial numbers
        if namespace.disablefilecheck is False:
            if not check_duplicates.check_config_duplicates(list_of_files):
                quit()
        else:
            print('!!!  ---- Unique files check is disabled ---- !!!')

        # Start processing of configs
        with alive_bar(len(list_of_files), length=55, title='Progress', force_tty=True) as bar:
            for file in list_of_files:
                if file == 'logfile.log':
                    continue
                bar.text = f'Processing file: {file}, please wait...'
                if os.path.isfile(file):
                    with open(file, "r", encoding='utf-8') as conffile:
                        config = conffile.read()
                        empty_device = copy.deepcopy(datamodel.config_entity)

                        # get basic parameters
                        regparsers.fill_devinfo_to_model_from_config(empty_device, config, file)   # add to model

                        txtfsmparsers.get_esi_to_model(empty_device, config, curr_path)

                        txtfsmparsers.get_macs_to_model(empty_device, config, curr_path)

                        txtfsmparsers.get_arps_to_model(empty_device, config, curr_path)

                        txtfsmparsers.get_ip_nei_to_model(empty_device, config, curr_path)

                        txtfsmparsers.get_bgp_routes_to_model(empty_device, config, curr_path)

                        empty_device['errors'], empty_device['known_errors'] = regparsers.check_error_log(empty_device['vendor_id'], config)
                        empty_device['all_errors'] = str(regparsers.count_all_errors_from_log(empty_device['vendor_id'], config))

                        empty_device['ecmp_groups'] = regparsers.obtain_ecmp_groups(empty_device['vendor_id'], config)
                        empty_device['hosts'] = regparsers.obtain_num_hosts(empty_device['vendor_id'], config)
                        empty_device['next_hops'] = regparsers.obtain_nexthops(empty_device['vendor_id'], config)
                        empty_device['routes'] = regparsers.obtain_route_num(empty_device['vendor_id'], config)

                        # get list of cdp neighbours
                        # not yet txtfsmparsers.get_cdp_neighbours_to_model(empty_device, config, curr_path)
                        # get list of ports with many MAC-addresses under them
                        # outintofiles.many_macs_file_output(config, curr_path, cdp_neighbours, devinfo)  # optional - to rework
                        # get interfaces configuration
                        # not yet txtfsmparsers.get_interfaces_config_to_model(empty_device, config, curr_path)
                        # not yet txtfsmparsers.get_vlans_configuration_to_model(empty_device, config, curr_path)
                        # add collected device data into array

                        devices.append(empty_device)
                bar()

        startTime = datetime.now()
        date = str(startTime.date()) + "-" + str(startTime.strftime("%H-%M-%S"))

        # print inventory data to screen and into cparser.csv file
        out_to_screen.print_devices_summary(devices)
        outintofiles.summary_file_output(devices)

        out_to_screen.print_devices_errors(devices)

        # print all macs to file all_macs.csv
        outintofiles.macs_to_file(devices)
        # print all arps to file all_arps.csv
        outintofiles.arps_to_file(devices)

        # print ip neighbours to file all_ip_neighbours.csv
        outintofiles.ip_neigh_to_file(devices)

        ############ DO ANALYTICS SWL01-SWL02 ###############
        same_stated_macs, absent_macs = analytics.compare_macs(devices, "TC-YAR-MD6-fab-swl01", "TC-YAR-MD6-fab-swl02")
        incompleted_arps, absent_arps = analytics.compare_arps(devices, "TC-YAR-MD6-fab-swl01", "TC-YAR-MD6-fab-swl02")

        same_stated_macs = analytics.remove_same_mac_dups(same_stated_macs)
        absent_macs = analytics.remove_absent_mac_dups(absent_macs)

        prefix = '_SWL01_SWL02'
        outintofiles.same_stated_macs_to_file(same_stated_macs, prefix)
        outintofiles.absent_macs_to_file(absent_macs, prefix)
        outintofiles.incompleted_arps_to_file(incompleted_arps, prefix)
        outintofiles.absent_arps_to_file(absent_arps, prefix)

        mh_pairs_stats = {
            'same_macs': len(same_stated_macs),
            'absent_macs': len(absent_macs),
            'incompleted_arps': len(incompleted_arps),
            'absent_arps': len(absent_arps),
            'ssmacs': same_stated_macs,
            'aarps': absent_arps,
            'iarps': incompleted_arps,
            'amacs': absent_macs
        }
        stats.append(mh_pairs_stats)

#        stats['swl01_swl02'].append('same_macs') = len(same_stated_macs)
#        stats['swl01_swl02'].append('absent_macs') = len(absent_macs)
#        stats['swl01_swl02'].append('incompleted_arps') = len(incompleted_arps)
#        stats['swl01_swl02'].append('absent_arps') = len(absent_arps)

        ############ DO ANALYTICS SWL03-SWL04 ################
        same_stated_macs, absent_macs = analytics.compare_macs(devices, "TC-YAR-MD6-fab-swl03", "TC-YAR-MD6-fab-swl04")
        incompleted_arps, absent_arps = analytics.compare_arps(devices, "TC-YAR-MD6-fab-swl03", "TC-YAR-MD6-fab-swl04")

        same_stated_macs = analytics.remove_same_mac_dups(same_stated_macs)
        absent_macs = analytics.remove_absent_mac_dups(absent_macs)

        prefix = '_SWL03_SWL04'
        outintofiles.same_stated_macs_to_file(same_stated_macs, prefix)
        outintofiles.absent_macs_to_file(absent_macs, prefix)
        outintofiles.incompleted_arps_to_file(incompleted_arps, prefix)
        outintofiles.absent_arps_to_file(absent_arps, prefix)

        mh_pairs_stats = {
            'same_macs': len(same_stated_macs),
            'absent_macs': len(absent_macs),
            'incompleted_arps': len(incompleted_arps),
            'absent_arps': len(absent_arps),
            'ssmacs': same_stated_macs,
            'aarps': absent_arps,
            'iarps': incompleted_arps,
            'amacs': absent_macs
        }
        stats.append(mh_pairs_stats)

        ############ DO ANALYTICS SWL05-SWL06 ################
        same_stated_macs, absent_macs = analytics.compare_macs(devices, "TC-YAR-MD6-fab-swl05", "TC-YAR-MD6-fab-swl06")
        incompleted_arps, absent_arps = analytics.compare_arps(devices, "TC-YAR-MD6-fab-swl05", "TC-YAR-MD6-fab-swl06")

        same_stated_macs = analytics.remove_same_mac_dups(same_stated_macs)
        absent_macs = analytics.remove_absent_mac_dups(absent_macs)

        prefix = '_SWL05_SWL06'
        outintofiles.same_stated_macs_to_file(same_stated_macs, prefix)
        outintofiles.absent_macs_to_file(absent_macs, prefix)
        outintofiles.incompleted_arps_to_file(incompleted_arps, prefix)
        outintofiles.absent_arps_to_file(absent_arps, prefix)

        mh_pairs_stats = {
            'same_macs': len(same_stated_macs),
            'absent_macs': len(absent_macs),
            'incompleted_arps': len(incompleted_arps),
            'absent_arps': len(absent_arps),
            'ssmacs': same_stated_macs,
            'aarps': absent_arps,
            'iarps': incompleted_arps,
            'amacs': absent_macs
        }
        stats.append(mh_pairs_stats)


        ############ DO ANALYTICS BR01-BR02 ################
        same_stated_macs, absent_macs = analytics.compare_macs(devices, "TC-YAR-MD6-fab-br01", "TC-YAR-MD6-fab-br02")
        incompleted_arps, absent_arps = analytics.compare_arps(devices, "TC-YAR-MD6-fab-br01", "TC-YAR-MD6-fab-br02")

        same_stated_macs = analytics.remove_same_mac_dups(same_stated_macs)
        absent_macs = analytics.remove_absent_mac_dups(absent_macs)

        prefix = '_BR01_BR02'

        outintofiles.same_stated_macs_to_file(same_stated_macs, prefix)
        outintofiles.absent_macs_to_file(absent_macs, prefix)
        outintofiles.incompleted_arps_to_file(incompleted_arps, prefix)
        outintofiles.absent_arps_to_file(absent_arps, prefix)

        mh_pairs_stats = {
            'same_macs': len(same_stated_macs),
            'absent_macs': len(absent_macs),
            'incompleted_arps': len(incompleted_arps),
            'absent_arps': len(absent_arps),
            'ssmacs': same_stated_macs,
            'aarps': absent_arps,
            'iarps': incompleted_arps,
            'amacs': absent_macs
        }
        stats.append(mh_pairs_stats)

        m1dyn_m2stat_a1reach_a2stale, m1dyn_m2stat_a1stale_a2reach, m1stat_m2dyn_a1reach_a2stale, m1stat_m2dyn_a1stale_a2reach, m1dyn_m2stat_a1reach_a2reach, m1stat_m2dyn_a1reach_a2reach, stat_m2stat_a1stale_a2stale, record_not_found = analytics.check_mac_arps(devices, "TC-YAR-MD6-fab-swl01", "TC-YAR-MD6-fab-swl02")
        outintofiles.macarpstates_to_file(date, devices, m1dyn_m2stat_a1reach_a2stale, m1dyn_m2stat_a1stale_a2reach, m1stat_m2dyn_a1reach_a2stale, m1stat_m2dyn_a1stale_a2reach, m1dyn_m2stat_a1reach_a2reach, m1stat_m2dyn_a1reach_a2reach, stat_m2stat_a1stale_a2stale, record_not_found)


        ############ ROUTING ANALYTICS ################
        # allfabric_routes = analytics.get_all_routes(devices)

        ############ REPORTING ################
        outintofiles.report_to_file(date, devices, stats)

        outintofiles.fab_stats_to_json(devices, stats)
        outintofiles.sw_stats_to_json(devices)

        # print all neighbours from all devices into 'all_neighbours_output.csv' file
        # not yet        outintofiles.all_neighbours_to_file(devices)
        # print links (connectivity) to all neighbours from all devices into file 'cdp_nei_output.csv'
        # not yet        outintofiles.connectivity_to_file(devices)

        # print interfaces info into file
        # not yet        outintofiles.interfaces_to_file(devices)

        # Trying to find missed devices that can be found in cdp data and save this to "missed_devices.csv" file
        # not yet        missed_devices = outintofiles.find_missed_devices()
        # not yet        outintofiles.missed_devices_file_output(missed_devices)

        #        if len(missed_devices) > 0:
        #            print('In CDP configuration we found mentioned {} devices, for whom we have no configurations.\n'
        #                  'See file \"missed.devices.csv\"'.format(len(missed_devices)))
        # analysis of required VLAN on trunk ports
        #        trunking_analisys()

        print("Finished processing files in folder: " + str(namespace.configdir) + '\n')

        # print devices summary
        out_to_screen.tbl_files_info_out2scr()


if __name__ == "__main__":
    main()
