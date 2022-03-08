# dns_update for bind9 DNS and Gandi Glue Record

The objective of this script is to update the DNS zone, restart the DNS service within the machine, update the Gandi glue record, and perform checks when the IP is different from the glue record

The script works in different steps:
1. Read the configuration files (config.json, logging.ini)
2. Check that the script has the right to read the DNS template zone file and the right to write the new zone within the DNS
3. Retrieve the public ip from the internet output stream by retrieving the information via https://api.myip.com
4. Recover the IP of the glue record within Gandi
5. Compare the 2 IPs
6. If the IPs are identical, the script will sleep for x minutes as defined by the configuration file via the `redo` variable before running the script again
7. If the IPs are different, the glue record within Gandi is updated
8. the template zone is loaded
9. The template zone is modified with a new serial number, the new IP
10. The new zone is written to the DNS zone directory
11. The DNS service is restarted

All actions are logged. If a request raises an exception, the script goes to sleep and waits x minutes defined by the `redo` variable before restarting. 

You can modify the logging system via the logging.ini file

## Deployment

### Automatic installation

Shell script to get the git repository in `/opt/dns_update` (install git if needed), install `Python3.8` and `bind9`. 

Also, a service file is added to the systemd services files. All you have to do is run `systemd start dns_update` to start the DNS update script.

After that, all you have to do is to set up the `config.json` file in order to successfully launch the dns update script

```shell
curl -s https://raw.githubusercontent.com/etidahouse/dns_update/main/set_up.sh | bash
```

### Install Part - pre-requisites 

To use or modify the project, you will need `python 3.8` and the `pip` dependency manager

Please do not forget to refer to the official documentation :
- Python 3.8 : https://docs.python.org/3.8/
- pip : https://pip.pypa.io/en/stable/

### Dependencies

#### pydantic

The project uses the pydantic library for management (read/write/object) in JSON.
An installation via the dependency manager is therefore necessary.

```bash
pip install pydantic
```

Please do not forget to refer to the official documentation : 
- https://pydantic-docs.helpmanual.io/ 

### Gandi

Please do not forget to refer to the official Gandi API documentation : 
- https://api.gandi.net/docs/

Get API Key (go to security part) :
- https://account.gandi.net/


## Settings Part

The project can be configured via different configuration files (`config.json`, `logging.ini`)

### 1. App Configuration

The `config.json` file placed in the source folder is used to set up parameters for the script.
The `config.json` file is made up as follows.

```json
{
    "api_key": "My-4P1-K3Y",
    "api_domain": "https://api.gandi.net/v5/domain/domains/{domain}/hosts",
    "api_ns": "https://api.gandi.net/v5/domain/domains/{domain}/hosts/{ns}",
    "domain_name": "domain-name.com",
    "domain_ns": "ns",
    "url_ip_address": "https://api.myip.com",
    "zone_dns_path": "/var/named/zone.my-domain.com",
    "cmd_restart_dns": "systemctl restart named",
    "redo": 10,
    "sleep_time": 5
}

```

Variable details :
- `api_key` : Represents the API KEY provided by Gandi to access these APIs
- `api_domain` : This route is used to find and return information about a domain to which you have permissions via Gandi API
- `api_ns` : This route returns information on a specific glue record for the given domain via Gandi API
- `domain_name` : Your domain name
- `domain_ns` : Your ns name
- `url_ip_address` : URL address to know your public ip
- `zone_template_path` : 
- `zone_dns_path` : Path of the directory where the DNS zone file will be written. This directory is the one used by your DNS to store the zones
- `cmd_restart_dns` : Represents the command to restart the DNS service 
- `redo` : Represents the time in minutes before the script is re-executed 
- `sleep_time` : Represents the time in minutes before the script is re-executed due to an error (e.g. no internet connection)

### 2. Logging Configuration

This file represents the configuration for the logging contained in the application. You can set the logging level, the name and destination of the log file, the log format, interval...

For more details about logging configuration in python 3.x, please, do not forget to refer to the official documentation: https://docs.python.org/3/library/logging.config.html

Example of configuration via ini file

```ini
[loggers]
keys=root

[logger_root]
level=DEBUG
handlers=screen,file

[formatters]
keys=simple,verbose

[formatter_simple]
format=%(asctime)s [%(levelname)s] %(name)s: %(message)s

[formatter_verbose]
format=[%(asctime)s] %(levelname)s [%(filename)s %(name)s %(funcName)s (%(lineno)d)]: %(message)s

[handlers]
keys=file,screen

[handler_file]
class=handlers.TimedRotatingFileHandler
interval=midnight
backupCount=5
formatter=verbose
level=DEBUG
args=('/var/log/dns_update/dns_update.log',)

[handler_screen]
class=StreamHandler
formatter=simple
level=DEBUG
args=(sys.stdout,)
```

### 3. zone.template

```
$TTL 86400
$ORIGIN ${DOMAIN.NAME}.
@ IN SOA ns.${DOMAIN.NAME}. hostmaster.${DOMAIN.NAME}. (
   {SN}   ; sn
        10800   ; refresh (3 heures)
          600   ; retry (10 minutes)
      1814400   ; expiry (3 semaines)
        10800   ; minimum (3 heures)
 )
        IN          NS      ns.${DOMAIN.NAME}.
        IN          NS      ns6.gandi.net.
        IN          MX      10 spool.mail.gandi.net.
begon.dev.          A       ${IP}
ns      IN          A       ${IP}
mail    IN          A       ${IP}
www     CNAME               ${DOMAIN.NAME}.
ftp     CNAME               ${DOMAIN.NAME}.
cloud   CNAME               ${DOMAIN.NAME}.
ssh     CNAME               ${DOMAIN.NAME}.
```

## Run

The main of the application is located in the file `main.py`. You just have to launch this python file with the default command.

```bash
 python3 main.py 
```

## Create systemd service

Create an new systemd service :

```bash
touch /etc/systemd/system/dns_update.service
```

Edit the service file : 

```
[Unit]
Description=dns_update

[Service]
ExecStart=/usr/bin/python3 /path/to/the/project/dns_update/main.py

[Install]
WantedBy=multi-user.targe
```

Start the systemd service :

```bash
systemctl start dns_update
```

Enable it :

```bash
systemctl enable dns_update
```
