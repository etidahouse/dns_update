import requests
import Configuration
import logging
import json


def get_ip_address(url_ip: str):
    logger = logging.getLogger(__name__)
    logger.info("Get IP Address to " + url_ip)
    ip_address = requests.request('GET', url_ip).json()
    logger.info("Current IP Address " + str(ip_address))
    return ip_address['ip']


def get_glue_record_info(glue_record_url: str, key: str):
    logger = logging.getLogger(__name__)
    logger.info('Get Glue Record Information to ' + glue_record_url)
    headers = {'authorization': 'Apikey ' + key}
    glue_record_info = requests.get(glue_record_url, headers=headers)
    if glue_record_info.status_code == 403:
        logger.error("Error, API Key is invalid, 403 status. message : " + str(glue_record_info.text))
        logging.error("Stopping process...")
        quit()
    elif glue_record_info.status_code != 200:
        logger.error("Error on HTTP request to glue record information, status : " + str(glue_record_info.status_code)
                     + " message : " + str(glue_record_info.text))
        logging.error("Stopping process...")
        quit()
    logger.info('Current Glue Record information ' + str(glue_record_info.text))
    for item in json.loads(glue_record_info.text):
        return item["ips"][0]


def update_glue_record(new_ip: str, glue_record_update_url: str, key: str):
    logger = logging.getLogger(__name__)
    logger.info("Update Glue Record IP Address with " + new_ip)
    headers = {'authorization': 'Apikey ' + key,
               'content-type': 'application/json'
               }
    payload = "{\"ips\":[\""+new_ip+"\"]}"
    response = requests.request("PUT", glue_record_update_url, data=payload, headers=headers)
    logger.info("Response to Gandi API : " + response.text)


def dns_update(conf: Configuration):
    logger = logging.getLogger(__name__)
    logger.info("Start NS update...")
    current_ip = get_ip_address(conf.url_ip_address)
    glue_record_ip = get_glue_record_info(conf.api_domain, conf.api_key)
    if current_ip != glue_record_ip:
        logger.info("The IP Address has changed. (current ip address : " + current_ip +
                    " - glue record ip address : " + glue_record_ip + ")")
        update_glue_record(current_ip, conf.api_ns, conf.api_key)
        return True
    else:
        logger.info("The IP Address has not changed. (current ip address : " + current_ip +
                    " - glue record ip address : " + glue_record_ip + ")")
        return False
