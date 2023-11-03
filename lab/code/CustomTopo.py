#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"

    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        Topo.__init__(self, **opts)

        self.__init_tree(
            fanout,
            level=0,
            parent=self.addSwitch("cs1"),
            level_info=[
                {"name": "as", "count": 0, "opts": linkopts1},
                {"name": "es", "count": 0, "opts": linkopts2},
                {"name": "hs", "count": 0, "opts": linkopts3},
            ],
        )

    def __init_tree(self, fanout, level, parent, level_info):
        if level >= len(level_info):
            return

        for index in range(fanout):
            info = level_info[level]
            info["count"] += 1
            name = info["name"] + str(info["count"])

            if level == len(level_info) - 1:
                device = self.addHost(name)
            else:
                device = self.addSwitch(name)

            self.addLink(device, parent, **info["opts"])

            self.__init_tree(fanout, level + 1, device, level_info)


def perfTest():
    opts = {
        "bw": 10,
        "delay": "5ms",
        "loss": 1,
        "max_queue_size": 1000,
        "use_htb": True,
    }
    topo = CustomTopo(opts, opts, opts)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()


if __name__ == "__main__":
    setLogLevel("info")
    perfTest()
