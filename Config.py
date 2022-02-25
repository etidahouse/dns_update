class Configuration:

    def __init__(self, api_key, api_domain, domain_name, api_ns, domain_ns, url_ip_address, zone_template_path,
                 zone_dns_path, cmd_restart_dns):
        self.__api_key = api_key
        api_domain = api_domain.replace("{domain}", domain_name)
        self.__api_domain = api_domain
        self.__domain_name = domain_name
        api_ns = api_ns.replace("{ns}", domain_ns).replace("{domain}", domain_name)
        self.__api_ns = api_ns
        self.__domain_ns = domain_ns
        self.__url_ip_address = url_ip_address
        self.__zone_template_path = zone_template_path
        self.__zone_dns_path = zone_dns_path
        self.__cmd_restart_dns = cmd_restart_dns

    @property
    def api_key(self):
        return self.__api_key

    @property
    def api_domain(self):
        return self.__api_domain

    @property
    def domain_name(self):
        return self.__domain_name

    @property
    def api_ns(self):
        return self.__api_ns

    @property
    def domain_ns(self):
        return self.__domain_ns

    @property
    def url_ip_address(self):
        return self.__url_ip_address

    @property
    def zone_template_path(self):
        return self.__zone_template_path

    @property
    def zone_dns_path(self):
        return self.__zone_dns_path

    @property
    def cmd_restart_dns(self):
        return self.__cmd_restart_dns

    def __str__(self):
        return "{'api_key':'" + self.__api_key + "', 'api_domain':'" + self.__api_domain + "', " + \
               "'domain_name':'" + self.__domain_name + "', 'api_ns':'" + self.__api_ns + "', " + \
               "'domain_ns':'" + self.__domain_ns + "', 'url_ip_address':'" + self.__url_ip_address + "', " +\
               "'zone_template_path':'" + self.__zone_template_path + "', " +\
               "'zone_dns_path':'" + self.__zone_dns_path + "'}"
