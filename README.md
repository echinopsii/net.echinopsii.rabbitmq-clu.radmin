net.echinopsii.rabbitmq-clu.radmin
==================================

This tool help you to configure RabbitMQ cluster remotely. Please note that this tool is totally unsecure (no authentication, no crypto ... just nothing)

It's done to automate dockerized RabbitMQ cluster setup (docker >= 1.5 & rabbimq >=3.5.0).

Usage example :


First start two rabbitmq containers :

```
user@myrabbit1 $ sudo docker run --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -d --name myrabbit1 --hostname myrabbit1 -p 5672:5672 -p 15672:15672 -p 1833:1833 -p 61613:61613 -p 4369:4369 -p 44001:44001 -p 127.0.0.1:5000:5000 echinopsii/fedora.21.systemd.rabbitmq
```
```
user@myrabbit2 $ sudo docker run --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -d --name myrabbit1 --hostname myrabbit1 -p 5672:5672 -p 15672:15672 -p 1833:1833 -p 61613:61613 -p 4369:4369 -p 44001:44001 -p 127.0.0.1:5000:5000 echinopsii/fedora.21.systemd.rabbitmq
```


Let's say myrabbit2 will connect to myrabbit1 to join the cluster :

```
user@myrabbit2 $ curl -i -H "Content-Type: application/json" -X POST -d '{"clusterName":"myrabbit1","primaryNodeFQDN":"myrabbit1.FQDN"}' http://localhost:5000/api/0.1/connect
```

```
user@myrabbit2 $ curl -i -H "Content-Type: application/json" -X POST -d '{"clusterName":"myrabbit1"}' http://localhost:5000/api/0.1/disconnect
```

Done.