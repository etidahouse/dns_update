import requests
import Config


def get_ip_address(url_ip: str):
    print("Get IP Address to " + url_ip)
    ip_address = requests.request('GET', url_ip).json()
    print("Current IP Address", ip_address)
    return ip_address['ip']


def get_glue_record_info(glue_record_url: str, key: str):
    print("Get Glue Record Information to", glue_record_url)
    headers = {'authorization': 'Apikey ' + key}
    glue_record_info = requests.request("GET", glue_record_url, headers=headers).json()
    print('Current Glue Record information', glue_record_info)
    for item in glue_record_info:
        return item['ips'][0]


def update_glue_record(new_ip: str, glue_record_update_url: str, key: str):
    print("Update Glue Record IP Address with "+new_ip)
    headers = {'authorization': 'Apikey ' + key,
               'content-type': 'application/json'
               }
    payload = "{\"ips\":[\""+new_ip+"\"]}"
    response = requests.request("PUT", glue_record_update_url, data=payload, headers=headers)
    print("Response to Gandi API : " + response.text)


def dns_update(conf: Config):
    print("Start NS update...")
    current_ip = get_ip_address(conf.url_ip_address)
    glue_record_ip = get_glue_record_info(conf.api_domain, conf.api_key)
    if current_ip != glue_record_ip:
        print("The IP Address has changed. (current ip address : " + current_ip + " - glue record ip address : " + glue_record_ip + ")")
        update_glue_record(current_ip, conf.api_ns, conf.api_key)
        return True
    else:
        print("The IP Address has not changed. (current ip address : " + current_ip + " - glue record ip address : " + glue_record_ip + ")")
        return False
