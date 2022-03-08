from pydantic import BaseModel
import logging

CONFIG_FILE_NAME = 'config.json'


class Configuration(BaseModel):
    api_key: str
    api_domain: str
    domain_name: str
    api_ns: str
    domain_ns: str
    url_ip_address: str
    zone_template_path: str
    zone_dns_path: str
    cmd_restart_dns: str

    def __init__(**kwargs):
        super().__init__(**kwargs)
        Configuration.api_domain = Configuration.api_domain.replace("{domain}", Configuration.domain_name)
        api_ns = Configuration.api_ns.replace("{ns}", Configuration.domain_ns).replace("{domain}",
                                                                                       Configuration.domain_name)


    def read_configuration() -> Configuration:
        logger = logging.getLogger(__name__)
        logger.debug("Read configuration file...")

        try:
            file = open(str(pathlib.Path().resolve()) + "/" + CONFIG_FILE_NAME, "r")
            data = json.load(file)
            conf: Configuration = Configuration(**data)

        except Exception as ex:
            logger.error('%s \n\t %s', ex, traceback.format_exc())
            raise RuntimeError("Error when parsing configuration file.", ex)

        file.close()
        logger.debug('%s \n\t %s', "Configuration loaded.", conf)
        return conf
