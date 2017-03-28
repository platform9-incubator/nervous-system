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
Insert correct rabbit password in rabbit:// url in glance-registry.conf template

## Run consul.
No config file here, everything on command line. Replace --advertise address
with your external address. Use the same command line for the third cluster
node.
```bash
./consul agent -server -data-dir=/root/consul-data -bootstrap-expect 3 --advertise 52.52.164.184 > logs/server.log 2>&1 &
```

## Run confd
```bash
./confd -watch=true -backend consul -node 127.0.0.1:8500 >> logs/confd.log 2>&1 &
```
