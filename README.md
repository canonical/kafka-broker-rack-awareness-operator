# Kafka Broker rack awareness Operator
[![Charmhub](https://charmhub.io/kafka-broker-rack-awareness/badge.svg)](https://charmhub.io/kafka-broker-rack-awareness)
[![Release](https://github.com/canonical/kafka-broker-rack-awareness-operator/actions/workflows/release.yaml/badge.svg)](https://github.com/canonical/kafka-broker-rack-awareness-operator/actions/workflows/release.yaml)
[![Tests](https://github.com/canonical/kafka-broker-rack-awareness-operator/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/canonical/kafka-broker-rack-awareness-operator/actions/workflows/ci.yaml)

Charmhub package name: Kafka Broker rack awareness

More information: https://charmhub.io/kafka-broker-rack-awareness

## Overview

This charm handles the configuration of the `broker.rack` setting for Kafka. It needs to be used alongside the [Kafka operator](https://charmhub.io/kafka).

## Usage

### Basic usage

The rack awareness Operator needs to be deployed to the same machine as the Kafka operator. First create a machine:
```shell
$ juju add-machine --series=jammy
```

Using `juju status`, get the number of the machine that was just created. If the model is empty it will be number 0.

```shell
$ juju deploy kafka --channel edge --to=0
$ juju deploy kafka-broker-rack-awareness --channel edge --to=0
```

Lastly, use `config` to set the `broker.rack` value:
```shell
$ juju config kafka-broker-rack-awareness broker-rack="my-value"
```

To watch the process, `juju status` can be used.


To specify different rack values, more than one rack awareness operator can be deployed. For example, if we have two brokers on a different zone each:

```shell
$ juju deploy kafka-broker-rack-awareness zone-one --channel edge --to=0  # machine of the first broker
$ juju deploy kafka-broker-rack-awareness zone-two --channel edge --to=1  # machine of the second broker

$ juju config zone-one broker-rack="zone-one"
$ juju config zone-two broker-rack="zone-two"
```

## Other resources

- [Contributing](CONTRIBUTING.md) <!-- or link to other contribution documentation -->

- See the [Juju SDK documentation](https://juju.is/docs/sdk) for more information about developing and improving charms.
