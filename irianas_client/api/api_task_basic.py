# This file is part of Irianas (Client).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import os
import hashlib
import socket
import simplejson as json
import psutil
import platform
import thread
from flask import request
from flask.ext.restful import Resource, abort
from irianas_client.system.basic_task_system import ShuttingSystem
from irianas_client.system.monitor_system import MonitorSystem
from irianas_client.decorators import require_token, path_file_token
from irianas_client.yumwrap.yumwrapper import YUMWrapper

ip_server = socket.gethostbyname(socket.gethostname())


class TaskBasicAPI(Resource):
    method_decorators = [require_token]

    def get(self, action):
        if action == 'shut':
            ShuttingSystem.shut_down()
        elif action == 'reboot':
            ShuttingSystem.reboot()
        elif action == 'suspend':
            ShuttingSystem.suspend()
        elif action == 'hibernate':
            ShuttingSystem.hibernate()
        elif action == 'update':
            thread.start_new_thread(YUMWrapper().update_system(), ())
        elif action == 'monitor':
            monitor = dict(cpu=int(MonitorSystem.get_cpu_porcent(3)),
                           memory=int(MonitorSystem.get_memory_used(True)),
                           disk=int(MonitorSystem.get_disk_used(True)))
            return monitor


class ClientInfoAPI(Resource):
    method_decorators = [require_token]

    def get(self):
        data = dict(host_name=platform.node(),
                    arch=platform.machine(),
                    os=platform.version(),
                    memory=psutil.virtual_memory()[0])
        return data


class ConnectAPI(Resource):
    m = hashlib.sha512()

    @require_token
    def get(self):
        if os.path.exists(path_file_token):
            os.remove(path_file_token)
            if not os.path.exists(path_file_token):
                return dict(logout=1)
            else:
                return dict(logout=0)
        else:
            return dict(logout=1)

    def post(self):
        if request.form.get('ip'):
            ip = hashlib.sha512(request.form.get('ip')).hexdigest()

            if os.path.exists(path_file_token):
                if request.form.get('token'):
                    token = hashlib.sha512(request.form['token']).hexdigest()
                else:
                    return abort(401)

            else:
                token_rand = os.urandom(64).encode('hex')
                token = hashlib.sha512(token_rand).hexdigest()
                dict_token = dict(token=token, ip=ip)
                file_token = open(path_file_token, 'w')
                json.dump(dict_token, file_token)

                return dict(token=token_rand)
