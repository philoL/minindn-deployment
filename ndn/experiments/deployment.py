# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2019, The University of Memphis,
#                          Arizona Board of Regents,
#                          Regents of the University of California.
#
# This file is part of Mini-NDN.
# See AUTHORS.md for a complete list of Mini-NDN authors and contributors.
#
# Mini-NDN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mini-NDN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mini-NDN, e.g., in COPYING.md file.
# If not, see <http://www.gnu.org/licenses/>.

from ndn.experiments.experiment import Experiment
from ndn.apps.routing_helper import IPRoutingHelper

from mininet.log import info


class DeployExperiment(Experiment):

    def __init__(self, args):
        Experiment.__init__(self, args)

    def start(self):
        self.setup()
        self.run()

    def setup(self):
        info("Experiment setup:")
        
        # Calculate all routes for IP routing
        IPRoutingHelper.calcAllRoutes(self.net)
        info("IP routes configured, start ping\n")
        self.net.pingAll()
        
        if self.options.isNlsrEnabled is True:
            self.startNlsr()

        for host in self.ol_hosts:
            info("node " + host.name + "\n")
            # Set strategy
            Nfdc.setStrategy(host, "/ndn/", self.options.strategy)

            # Start ping server
            info("Start ndnping servers")
            host.cmd("ndnpingserver /ndn/{}-site/{} > ping-server &".format(host.name, host.name))

            # Create folder to store ping data
            host.cmd("mkdir ping-data")

    def run(self):
        pass

Experiment.register("deploy", DeployExperiment)

