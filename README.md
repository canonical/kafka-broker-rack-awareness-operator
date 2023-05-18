# Kafka Broker rack awareness Operator

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
$ juju deploy kafka-broker-rack-awareness --channel edge --to=0 --config 
```

Lastly, use `config` to set the `broker.rack` value:
```shell
$ juju config kafka-broker-rack-awareness broker-rack="my-value"
```

To watch the process, `juju status` can be used.

## Other resources

- [Contributing](CONTRIBUTING.md) <!-- or link to other contribution documentation -->

- See the [Juju SDK documentation](https://juju.is/docs/sdk) for more information about developing and improving charms.
