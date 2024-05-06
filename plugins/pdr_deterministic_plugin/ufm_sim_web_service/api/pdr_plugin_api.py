#
# Copyright © 2013-2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#

import re
import time

from flask import request
from utils.flask_server.base_flask_api_server import BaseAPIApplication

class PDRPluginAPI(BaseAPIApplication):
    '''
    class PDRPluginAPI
    '''

    def __init__(self, isolation_mgr):
        """
        Initialize a new instance of the PDRPluginAPI class.
        """
        super(PDRPluginAPI, self).__init__()
        self.isolation_mgr = isolation_mgr


    def _get_routes(self):
        """
        Map URLs to function calls
        """
        return {
            self.get_excluded_ports: dict(urls=["/excluded"], methods=["GET"]),
            self.exclude_ports: dict(urls=["/excluded"], methods=["PUT"]),
            self.include_ports: dict(urls=["/excluded"], methods=["DELETE"])
        }


    def get_excluded_ports(self):
        """
        Return ports from exclude list as comma separated port names
        """
        items = self.isolation_mgr.exclude_list.items()
        formatted_items = [f"{item.port_name}: {'infinite' if item.ttl_seconds == 0 else int(max(0, item.remove_time - time.time()))}" for item in items]
        return '\n'.join(formatted_items) + ('' if not formatted_items else '\n')


    def exclude_ports(self):
        """
        Parse input ports and add them to exclude list (or just update TTL)
        Input string example: 0c42a10300756a04_1,98039b03006c73ba_2:300
        TTL that follows port name after the colon is optional
        """
        data_dict = request.form.to_dict()
        if not data_dict:
            return "No ports added to exclude list"
      
        response = ""
        excluded_pors_str = next(iter(data_dict.keys()))
        pair_pattern = re.compile(r'\((.*?)(?:,(.*?))?\)')
        pairs = pair_pattern.findall(excluded_pors_str)
        for pair in pairs:
            if pair[0].strip():
                port_name = pair[0].strip()
                ttl = 0 if not pair[1].strip().isdigit() else int(pair[1].strip())
                self.isolation_mgr.exclude_list.add(port_name, ttl)
                response += f"Port {port_name} added to exclude list\n"

        return response


    def include_ports(self):
        """
        Remove ports from exclude list
        Input string: comma separated port names
        """
        data_dict = request.form.to_dict()
        if not data_dict:
            return "No ports removed from exclude list"
      
        port_names_str = next(iter(data_dict.keys()))
        port_names = re.findall(r'\w+', port_names_str)
        response = ""
        for port_name in port_names:
            if port_name.strip():
                port_name = port_name.strip();
                if self.isolation_mgr.exclude_list.remove(port_name):
                    response += f"Port {port_name} removed from exclude list\n"
                else:
                    response += f"Port {port_name} is not in exclude list\n"
        
        return response