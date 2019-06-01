# Overview

This is an example of an Open Source Mano (OSM) Network Service (ns) charm. This is an **experimental** feature, expected to be released with OSM R6 in the spring of 2019.

This allows a charm to coordinate the execution of [actions] across multiple charms within a model.

# Usage

# Application Names

Each deployed application is named using a set of runtime variables, such as the network service name, the vnf or vdu name, and the vnf-member-index. Because of that, we'll need to provide those values to the NS charm through its configuration.

# Configuration

The `config.yaml` file contains a mapping of properties that will be passed from OSM to your deployed charm. Some of those properties are automatically included by the underlying `osm-ns` layer:
- juju-username
- juju-password

You'll need to pass the name of the network service that you deployed. Even though your network service may be named `nscharm` in the descriptor, the operator provides a name at instantiation time, and `osm-ns` needs this name in order to resolve the application names. You can call it anything you like, as long as it's consistent between the NS charm and the NS Descriptor.

For each VNF or VDU with a charm you wish to interact with, you need to also pass it's id from the VNF Descriptor. Again, you can call this anything you like, as long as it's consistent between the NS charm and NS Descriptor.

`config.yaml`:
```yaml
options:
    nsr-name:
        default:
        description: The runtime name of the Network Service, i.e., what its deployed name is.
        type: string

    user-member-index:
        default:
        description: The vnf-member-index of the user VNF.
        type: string
    user-vdu-id:
        default:
        description: The id of the VDU containing the charm.
        type: string

    policy-member-index:
        default:
        description: The vnf-member-index of the policy VNF.
        type: string
    policy-vdu-id:
        default:
        description: The id of the VDU containing the charm.
        type: string
```

# NS Descriptor

The NS descriptor contains a new `ns-configuration` element, similar to that of `vnf-configuration` and `vdu-configuration` available in VNF descriptors.

The key here is to pass the juju credentials from your environment, available in `~/.local/share/juju/accounts.yaml`. This enables the charm to speak directly to Juju, via the `osm-ns` layer.

Next, you must map the runtime parameters of your Network Service so that the charm is aware of your topology.

Lastly, you can then define the primitives, under `config-primitive`, to be available to the operator for day-2 operation.

```yaml
        ns-configuration:
            juju:
                charm: ns
            initial-config-primitive:
            -   seq: '1'
                name: config
                parameter:
                # Configure Juju credentials
                -   name: juju-username
                    value: 'admin'
                -   name: juju-password
                    value: '50b4491a7a42d3542e317e3ae94c6c96'

                # Set the runtime name of the network service
                -   name: nsr-name
                    value: 'test'

                # For each vnf, map the vnf-member-index and vdu-id
                -   name: user-member-index
                    value: '1'
                -   name: user-vdu-id
                    value: 'userVM'

                -   name: policy-member-index
                    value: '2'
                -   name: policy-vdu-id
                    value: 'policyVM'

            -   seq: '2'
                name: add-user
                parameter:
                -   name: username
                    value: root
            config-primitive:
            -   name: add-user
                parameter:
                -   name: username
                    data-type: STRING
```

## Known Limitations and Issues

This functionality is EXPERIMENTAL.

# Configuration

# Contact Information


## Open Source Mano (OSM)

  - [OSM website](https://osm.etsi.org/)
  - [OSM bug tracker](https://osm.etsi.org/bugzilla/)
  - [OSM_TECH](mailto:OSM_TECH@list.etsi.org) mailing list
  - [Slack](https://join.slack.com/t/opensourcemano/shared_invite/enQtMzQ3MzYzNTQ0NDIyLWJkMzRjNDM0MjFjODYzMGQ3ODIzMzJlNTg2ZGI5OTdiZjFiNDMyMzYxMjRjNDU4N2FmNjRjNzY5NTE1MjgzOTQ)

[actions]: https://docs.jujucharms.com/2.5/en/actions
