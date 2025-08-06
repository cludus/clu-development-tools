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