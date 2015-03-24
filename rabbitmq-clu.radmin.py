#!/usr/bin/python3
#
# net.echinopsii.rabbitmq-clu.radmin
#
# Copyright (C) 2015 Mathilde Ffrench
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from os import abort
import os
import shutil
import socket
import subprocess

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)
app.debug = True

@app.route('/')
def running():
    return 'RabbitMQ Cluster REST admin is running !'


@app.route('/api/0.1/setUpHosts', methods=['POST'])
def setup_dns():
    if not request.json:
        abort(400)

    cluster_nodes_definition = request.json
    print cluster_nodes_definition
    if cluster_nodes_definition is None:
        abort(400)
    else:
        if not os.path.isfile("/etc/hosts.orig"):
            shutil.copyfile("/etc/hosts", "/etc/hosts.orig")

        shutil.copyfile("/etc/hosts.orig", "/etc/hosts")

        for node_definition in cluster_nodes_definition:
            node_name = node_definition.get('nodeName')
            node_fqdn = node_definition.get('nodeFQDN')

            ip = None
            ais = socket.getaddrinfo(node_fqdn, 0, 0, 0, 0)
            for result in ais:
                ip = str(result[-1][0])
                break

            host_entry = ip + "    " + node_name
            add_host_entry_cmd = "echo \"" + host_entry + "\" >> /etc/hosts"
            ret = subprocess.call(add_host_entry_cmd, shell=True)

        return jsonify(result={"status": 200})

@app.route('/api/0.1/cleanHosts', methods=['POST'])
def clean_dns():
    if os.path.isfile("/etc/hosts.orig"):
        shutil.copyfile("/etc/hosts.orig", "/etc/hosts")
    return jsonify(result={"status": 200})

@app.route('/api/0.1/connect', methods=['POST'])
def connect_cluster():
    if not request.json:
        abort(400)

    cluster_name = str(request.json.get('clusterName'))

    if cluster_name is None:
        abort(400)
    else:
        ret = subprocess.call("rabbitmqctl stop_app", shell=True)
        join_cluster_cmd = "rabbitmqctl join_cluster rabbit@" + cluster_name
        ret = subprocess.call(join_cluster_cmd, shell=True)
        ret = subprocess.call("rabbitmqctl start_app", shell=True)

        return jsonify(result={"status": 200, "info": 'Connected To Cluster ' + cluster_name + '!'})

@app.route('/api/0.1/disconnect', methods=['POST'])
def disconnect_cluster():
    if not request.json:
        abort(400)

    cluster_name = str(request.json.get('clusterName'))

    if cluster_name is None:
        abort(400)
    else:
        ret = subprocess.call("rabbitmqctl stop_app", shell=True)
        ret = subprocess.call("rabbitmqctl reset", shell=True)
        ret = subprocess.call("rabbitmqctl start_app", shell=True)

        return jsonify(result={"status": 200, "info": 'Disconnected From Cluster ' + cluster_name + ' !'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
