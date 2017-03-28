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

* Update 'advertise_addr' with r1's ip address in consul-config.json
* Insert correct rabbit password in rabbit:// url in glance-registry.conf template.

## Run consul
```bash
./consul agent -config-file consul-config.json > logs/server.log 2>&1 &
```

## Run confd
```bash
./confd -watch=true -backend consul -node 127.0.0.1:8500 >> logs/confd.log 2>&1 &
```

## Join cluster servers
After all the cluster nodes are up:
```bash
./consul join 54.67.110.172 52.52.164.184
```
supplying the addresses of the other two nodes. You only have to do this
on one node.

## Add keystone admin_token to consul (needed by update_password.py)
```bash
./consul kv put admin_token 1234abcd
```
