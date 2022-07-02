import dns_update
import zone_dns
import os
import time
import logging.config
from Configuration import *
import schedule


def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting...")
    conf: Configuration = read_configuration()
    check_file_permission(str(os.path.dirname(os.path.abspath(__file__))) + "/files/zone.template", os.R_OK)
    check_directory_permission(conf.zone_dns_path, os.W_OK)
    schedule.every(conf.redo).minutes.do(action, conf)
    while True:
        try:
            schedule.run_pending()
            time.sleep(conf.sleep_time * 60)
        except Exception as ex:
            logger.error('%s \n\t %s', ex, traceback.format_exc())
            logger.info("Sleep for " + conf.sleep_time + " minutes")
            time.sleep(conf.sleep_time * 60)
            continue


def action(conf: Configuration):
    logger = logging.getLogger(__name__)
    new_ip = dns_update.dns_update(conf)
    if new_ip:
        logger.info('Change DNS zone file...')
        zone_dns.change_zone_dns(dns_update.get_ip_address(conf.url_ip_address), conf)
        logger.info('Restart DNS service...')
        os.system(conf.cmd_restart_dns)
        logger.info('End of update.')
    else:
        logger.info('End of update.')


if __name__ == '__main__':
    logging.config.fileConfig(str(os.path.dirname(os.path.abspath(__file__))) + "/" + 'files/logging.ini')
    main()
