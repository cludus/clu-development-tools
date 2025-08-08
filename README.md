# Install

    wget -qO- 'https://api.github.com/repos/cludus/clu-development-tools/releases/latest' | jq -r '.tarball_url' | xargs wget -qO- > cludt.tar.gz
    tar -xvzf cludt.tar.gz
    cd cludus-clu-development-tools-...
    pip install build
    python -m build
    cd dist
    pip install cludt-<...>.whl

# Usage

To create a new k8s cluster, here is an example of cluster.yml

```yaml
name: mykube-clust
subnet_prefix: 10.64.0
domain_name: mykube.private
cpus: 2
node_memory: 4
node_disk: 20
certificate:
  country: US
  state: Some State
  city: Some City
  organization: Cludus
  organization_unit: MyKube Cluster
nodes:
  - type: master
  - type: server
  - type: server
  - type: agent
  - type: agent
  - type: agent
  - type: agent
```

Then run the following command to create a local cluster

    cludt k8s init local

