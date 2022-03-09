from pydantic import BaseModel
import logging
import json
import traceback
import os

CONFIG_FILE_NAME = 'config.json'


class Configuration(BaseModel):
    api_key: str
    api_domain: str
    api_ns: str
    domain_name: str
    domain_ns: str
    url_ip_address: str
    zone_dns_path: str
    cmd_restart_dns: str
    redo: int
    sleep_time: int


def read_configuration() -> Configuration:
    logger = logging.getLogger(__name__)
    logger.debug("Read configuration file...")

    try:
        file = open(str(os.path.dirname(os.path.abspath(__file__))) + "/" + CONFIG_FILE_NAME, "r")
        data = json.load(file)
        conf: Configuration = Configuration(**data)

        conf.api_domain = conf.api_domain.replace("{domain}", conf.domain_name)
        conf.api_ns = conf.api_ns.replace("{ns}", conf.domain_ns).replace("{domain}", conf.domain_name)

    except Exception as ex:
        logger.error('%s \n\t %s', ex, traceback.format_exc())
        raise RuntimeError("Error when parsing configuration file.", ex)

    file.close()
    logger.debug('%s \n\t %s', "Configuration loaded.", conf)
    return conf


def check_directory_permission(directory: str, permission):
    logger = logging.getLogger(__name__)
    logger.info("Checking permission for the directory : " + directory)
    try:
        if not os.path.isdir(directory):
            logger.error("Error, " + directory + " is not a directory")
            raise Exception("Error, " + directory + " is not a directory")
        if not os.access(directory, permission):
            logger.error("Error, not read permission to " + directory)
            raise Exception("Error, not read permission to " + directory)
    except Exception as ex:
        logger.error('%s \n\t %s', ex, traceback.format_exc())
        raise Exception(ex)


def check_file_permission(file: str, permission):
    logger = logging.getLogger(__name__)
    logger.info("Checking permission for the file : " + file)
    try:
        if not os.access(file, permission):
            logger.error("Error, not read permission to " + file)
            raise Exception("Error, not read permission to " + file)
    except Exception as ex:
        logger.error('%s \n\t %s', ex, traceback.format_exc())
        raise Exception(ex)
