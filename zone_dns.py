import time
import Configuration
import logging


def read_zone_template(zone_template_path: str):
    logger = logging.getLogger(__name__)
    logger.info("Read Zone Template file...")
    zone_file = open(zone_template_path, 'r')
    value = zone_file.read()
    zone_file.close()
    return value


def config_zone(zone_value: str, ip: str, conf: Configuration):
    logger = logging.getLogger(__name__)
    logger.info('Config zone...')
    logger.info('IP write in zone_value : ' + ip)
    zone_value = zone_value.replace('${IP}', ip)
    serial = time.strftime('%Y%m%d%H')
    logger.info('Serial Number write in zone_value : ' + serial)
    zone_value = zone_value.replace('${SN}', serial)
    logger.info("Domain name value is : " + conf.domaine_name)
    zone_value = zone_value.replace("${DOMAIN.NAME}", conf.domaine_name)
    return zone_value


def write_zone(zone_file: str, zone_value: str):
    logger = logging.getLogger(__name__)
    logger.info("Write zone dns  " + zone_file)
    fo = open(zone_file, "w")
    fo.write(zone_value)
    fo.close()


def change_zone_dns(ip: str, conf: Configuration):
    zone = read_zone_template(conf.zone_template_path)
    zone = config_zone(zone, ip, conf)
    write_zone(conf.zone_dns_path, zone)
