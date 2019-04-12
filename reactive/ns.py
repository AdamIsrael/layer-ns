"""asdfself"""
from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    status_set,
    log,
    config,
)

from charms.reactive import (
    clear_flag,
    set_flag,
    when,
    when_not,
)
import charms.osm.ns


@when_not('ns.installed')
def install_ns():
    set_flag('ns.installed')


@when('actions.add-user')
def action_add_user():
    """Add a user to the database."""
    err = ''
    output = ''
    try:
        username = action_get('username')
        bw = action_get('bw')
        qos = action_get('qos')
        tariff = action_get('tariff')

        log("Connecting to Juju")

        # Get the configuration, which should contain the juju username and
        # password. The endpoint and model will be discovered automatically
        cfg = config()

        client = charms.osm.ns.NetworkService(
            user=cfg['juju-username'],
            secret=cfg['juju-password'],
        )

        user_id = add_user(client, username, tariff)
        if user_id > 0:
            success = set_policy(client, user_id, bw, qos)
        else:
            log("user_id is 0; add_user failed.")

        log("Output from charm: {}".format(output))

    except Exception as err:
        log(str(err))
        action_fail(str(err))
    else:
        action_set({
            'user-id': user_id,
            'policy-set': success,
        })
    finally:
        clear_flag('actions.add-user')


def add_user(client, username, tariff):
    """Add a user to the database and return the id."""

    output = client.ExecutePrimitiveGetOutput(
        # The name of the charm responsible for adding a user
        "vnf-user",
        # The name of the action to call
        "add-user",
        # The parameter(s) required by the above charm and action
        params={
            'username': username,
            'tariff': tariff,
        },
        # How long to wait (in seconds) for the action to finish
        timeout=500
    )

    # Get the output from the `add-user` function
    user_id = int(output['user-id'])
    return user_id


def set_policy(client, user_id, bw, qos):
    """Set the policy for a user."""
    success = False

    success = client.ExecutePrimitiveGetOutput(
        "vnf-policy",
        "set-policy",
        params={
            'user_id': user_id,
            'bw': bw,
            'qos': qos,
        },
        timeout=500
    )

    return success
