## Get consul and confd
```bash
$ wget https://releases.hashicorp.com/consul/0.7.5/consul_0.7.5_linux_amd64.zip
$ unzip consul_0.7.5_linux_amd64.zip
$ wget https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64
$ ln -s confd-0.11.0-linux-amd64 confd
```

## directories
```bash
$ mkdir -p {logs,consul-data}
```

## config
Insert correct rabbit_password in imagelibrary.conf template.

## Run consul
Use the host's public advertise address and join with one of the cluster
servers (ie one of the DUs or the 3rd quorum member)
```bash
./consul agent -data-dir /root/consul-data -advertise 10.4.253.76 -join 52.53.53.62 > logs/client.log 2>&1 &
```

## Run confd
```bash
./confd -watch=true -backend consul -node 127.0.0.1:8500 >> logs/confd.log 2>&1 &
```
