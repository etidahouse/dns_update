import time
import Config


def read_zone_template(zone_template_path: str):
    print("Read Zone Template file...")
    zone_file = open(zone_template_path, 'r')
    value = zone_file.read()
    zone_file.close()
    return value


def config_zone(zone_value: str, ip: str):
    print('Config zone...')
    print('IP write in zone_value : ' + ip)
    zone_value = zone_value.replace('{IP}', ip)
    serial = time.strftime('%Y%m%d%H')
    print('Serial Number write in zone_value : ' + serial)
    zone_value = zone_value.replace('{SN}', serial)
    return zone_value


def write_zone(zone_file: str, zone_value: str):
    print("Write zone dns  " + zone_file)
    fo = open(zone_file, "w")
    fo.write(zone_value)
    fo.close()


def change_zone_dns(ip: str, conf: Config):
    zone = read_zone_template(conf.zone_template_path)
    zone = config_zone(zone, ip)
    write_zone(conf.zone_dns_path, zone)
