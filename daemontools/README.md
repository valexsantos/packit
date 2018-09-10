# Daemontools Slackware / CentOS package

daemontools-encore package for Slackware and Centos 6 / 7

## Usage

* Slackware (as root)

```
make slack
```

* Redhat and clones

```
make rpm
```

## systemd

One of these days the backup system failed in one of the servers:

```
# systemctl status bareos-storage.service 
● bareos-sd.service - Bareos Storage Daemon service
   Loaded: loaded (/usr/lib/systemd/system/bareos-sd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2018-01-15 
     Docs: man:bareos-sd(8)
  Process: 2473 ExecStart=/usr/sbin/bareos-sd (code=exited, status=0/SUCCESS)
 Main PID: 2477 (ntpd)
   CGroup: /system.slice/bareos-sd.service
           ‣ 2477 /usr/sbin/ntpd -u ntp:ntp -g
...
```

So, I include a unit to run daemontools as a systemd service.

```
[Unit]
Description=DJB daemontools
# After=sysinit.target
After=systemd-remount-fs.service

[Service]
ExecStart=_PREFIX_/svscanboot
Restart=always

[Install]
WantedBy=multi-user.target
```


