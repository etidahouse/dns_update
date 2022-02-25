import dnsupdate
import json
from Config import *
import zoneDNS
import os
import time
import logging.config


def read_configuration():
    logger = logging.getLogger(__name__)
    logger.info("Read configuration file...")
    file = open(CONFIG_FILE_NAME)
    data = json.load(file)
    api_key = data[CONFIG_OBJECT][CONFIG_ATTR_API_KEY]
    api_domain = data[CONFIG_OBJECT][CONFIG_ATTR_API_DOMAIN]
    domain_name = data[CONFIG_OBJECT][CONFIG_ATTR_DOMAIN_NAME]
    api_ns = data[CONFIG_OBJECT][CONFIG_ATTR_API_NS]
    domain_ns = data[CONFIG_OBJECT][CONFIG_ATTR_DOMAIN_NS]
    url_ip_address = data[CONFIG_OBJECT][CONFIG_ATTR_URL_IP_ADDRESS]
    zone_template_path = data[CONFIG_OBJECT][CONFIG_ATTR_ZONE_TEMPLATE_PATH]
    zone_dns_path = data[CONFIG_OBJECT][CONFIG_ATTR_ZONE_DNS_PATH]
    cmd_restart_dns = data[CONFIG_OBJECT][CONFIG_ATTR_CMD_RESTART_DNS]
    file.close()
    logger.info("Return Configuration Object...")
    c = Configuration(api_key, api_domain, domain_name, api_ns, domain_ns, url_ip_address, zone_template_path,
                      zone_dns_path, cmd_restart_dns)
    logging.debug(c.__str__())
    return c


def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting...")
    conf = read_configuration()
    while 1:
        new_ip = dnsupdate.dns_update(conf)
        if new_ip:
            logger.info('Change DNS zone file...')
            zoneDNS.change_zone_dns(dnsupdate.get_ip_address(conf.url_ip_address), conf)
            logger.info('Restart DNS service...')
            os.system(conf.cmd_restart_dns)
            logger.info('End of update.')
        else:
            logger.info('End of update.')
        time.sleep(60)


if __name__ == '__main__':
    logging.config.fileConfig('files/logging.ini')
    main()

