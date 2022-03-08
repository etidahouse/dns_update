# dns_update









## Deployement

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

## Settings Part

The project can be configured via different configuration files (`config.json`, `logging.ini`)

### 1. App Configuration

The `config.json` file placed in the source folder is used to set up the `elastic` server host and certain application behaviours.
The `config.json` file is made up as follows.

```json
{
    "api_key": "My-4P1-K3Y",
    "api_domain": "https://api.gandi.net/v5/domain/domains/{domain}/hosts",
    "api_ns": "https://api.gandi.net/v5/domain/domains/{domain}/hosts/{ns}",
    "domain_name": "domain-name.com",
    "domain_ns": "ns",
    "url_ip_address": "https://api.myip.com",
    "zone_template_path": "/path/to/dnsupdate/zone.template",
    "zone_dns_path": "/var/named/zone.my-domain.com",
    "cmd_restart_dns": "systemctl restart named",
    "redo": 10,
    "sleep_time": 5
}

```

Variable details :


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
$ORIGIN begon.dev.
@ IN SOA ns.begon.dev. hostmaster.begon.dev. (
   {SN}   ; sn
        10800   ; refresh (3 heures)
          600   ; retry (10 minutes)
      1814400   ; expiry (3 semaines)
        10800   ; minimum (3 heures)
 )
        IN          NS      ns.begon.dev.
        IN          NS      ns6.gandi.net.
        IN          MX      10 spool.mail.gandi.net.
begon.dev.          A       ${IP}
ns      IN          A       ${IP}
mail    IN          A       ${MAIL.IP}
www     CNAME               begon.dev.
ftp     CNAME               begon.dev.
cloud   CNAME               begon.dev.
ssh     CNAME               begon.dev.
```

## Run

The main of the application is located in the file `main.py`. You just have to launch this python file with the default command.

```bash
 python3 main.py 
```

## Create systemd service

```bash
touch /etc/systemd/system/dns_update.service
```

Edit the service file : 

Create an new systemd service :

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
