# data-analysis-flask-dashboard
Gather and Plot granular OS statistics in flask dashboard

# Dashboard preview

![flash-data-analysis-dashboard](https://github.com/idanaila/data-analysis-flask-dashboard/assets/47727784/14e5c48f-c9ac-47c1-bd56-f6695bae5801)

# Install
The statistics are collected from the target nodes via a Python script running as a systemctl service. The logs are rotated every 20MB and 5 files.
It will be deployed as an ansible playbook. For this setup we need a master node(use a custom user instead of root). The target hosts shall be added in /etc/hosts on the master.
```
$ ansible-playbook monarch.yaml
```
