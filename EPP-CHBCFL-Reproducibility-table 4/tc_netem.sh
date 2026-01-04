#!/bin/bash

IFACE=docker0

tc qdisc del dev $IFACE root 2>/dev/null

tc qdisc add dev $IFACE root netem delay 10ms 2ms loss 0.1%

tc qdisc add dev $IFACE parent 1:1 handle 10: tbf \
  rate 100mbit burst 32kbit latency 400ms
