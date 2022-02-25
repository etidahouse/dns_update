import dnsupdate
import json
import Config
import zoneDNS
import os
import time
import logging.config

CONFIG_FILE_NAME = 'config.json'
CONFIG_OBJECT = 'config'
CONFIG_ATTR_API_KEY = "gandi.api.key"
CONFIG_ATTR_API_DOMAIN = "gandi.api.domain"
CONFIG_ATTR_DOMAIN_NAME = "domain.name"
CONFIG_ATTR_API_NS = "gandi.api.update.glue.record.ip"
CONFIG_ATTR_DOMAIN_NS = "domain.ns"
CONFIG_ATTR_URL_IP_ADDRESS = "url.ip.address"
CONFIG_ATTR_ZONE_TEMPLATE_PATH = "path.zone.template"
CONFIG_ATTR_ZONE_DNS_PATH = "path.zone.dns"
CONFIG_ATTR_CMD_RESTART_DNS = "cmd.restart.dns"


def read_configuration():
    logger = logging.getLogger(__name__)
    logging.debug("Read configuration file...")
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
    logging.debug("Return Configuration Object...")
    c = Config.Configuration(api_key, api_domain, domain_name, api_ns, domain_ns, url_ip_address,
                             zone_template_path, zone_dns_path, cmd_restart_dns)
    logging.debug(c.__str__())
    return c


if __name__ == '__main__':
    logging.config.fileConfig('files/logging.ini')
    logging.debug("Starting...")
    conf = read_configuration()
    while 1:
        new_ip = dnsupdate.dns_update(conf)
        if new_ip:
            logging.debug('Change DNS zone file...')
            zoneDNS.change_zone_dns(dnsupdate.get_ip_address(conf.url_ip_address), conf)
            logging.debug('Restart DNS service...')
            os.system(conf.cmd_restart_dns)
            logging.debug('End of update.')
        else:
            logging.debug('End of update.')
        time.sleep(60)
