# Copyright 2026 Roger Joys
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

import requests

from .api import UnifiAPI
from .enums import HTTPCall, UnifiApiClass, UnifiCommandManager, UnifiEndpointSymbolics

logger = logging.getLogger(__name__)


class UnifiUtils:

    def __init__(self, endpoint: str, api_key: str, site: str) -> None:
        self.endpoint = endpoint
        self.api_key = api_key
        self.site = site
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        })

    def make_api_call(
        self,
        api_call: UnifiAPI,
        json_body: dict | None = None,
        added_substitutions: dict[UnifiEndpointSymbolics, str] | None = None,
        mac_address: str | None = None,
    ) -> dict:
        logger.debug("Entering: make_api_call")
        logger.debug("json_body: %s", json_body)

        # Handle mac_address shorthand: build command body for callable commands
        if mac_address is not None and json_body is None:
            if api_call.api_class == UnifiApiClass.CallableCommand:
                json_body = json.loads(self._create_command_body(api_call, mac_address))
                logger.debug("Posting body of: %s", json_body)
            else:
                json_body = {}

        uri_string = self._build_uri(api_call)
        logger.debug("Initial URI String: %s", uri_string)
        logger.debug("The APICall is: %s", api_call.name)
        logger.debug("The HTTPCall is: %s", api_call.call_type)
        logger.debug("The Command Manager is: %s", api_call.command_manager.manager)

        substitutions: dict[UnifiEndpointSymbolics, str] = {}
        logger.debug("Adding Site to Symbolics")
        substitutions[UnifiEndpointSymbolics.Site] = self.site

        if api_call.command_manager != UnifiCommandManager.Non:
            logger.debug("Adding Manager to Symbolics")
            substitutions[UnifiEndpointSymbolics.Manager] = api_call.command_manager.manager

        if added_substitutions:
            for symbolic, value in added_substitutions.items():
                logger.debug("Adding additional symbolic: %s Value: %s", symbolic.symbolic, value)
                substitutions[symbolic] = value

        url = self._substitute_symbolics(uri_string, substitutions)
        logger.debug("Making call: %s %s", api_call.name, url)

        call_type = api_call.call_type

        if call_type == HTTPCall.GET:
            response = self.session.get(url)
        elif call_type == HTTPCall.POST:
            if api_call.api_class == UnifiApiClass.CallableCommand and json_body is None:
                body_str = self._create_command_body(api_call, None)
            else:
                body_str = json.dumps(json_body) if json_body is not None else "{}"
            response = self.session.post(url, data=body_str)
        elif call_type == HTTPCall.PUT:
            body_str = json.dumps(json_body) if json_body is not None else "{}"
            response = self.session.put(url, data=body_str)
        elif call_type == HTTPCall.DELETE:
            response = self.session.delete(url)
        elif call_type == HTTPCall.HEAD:
            response = self.session.head(url)
            return {}
        else:
            raise ValueError(f"Unsupported HTTP method: {call_type}")

        logger.debug("Status is %s", response.status_code)
        logger.debug("Body is: %s", response.text)

        json_response = response.json()
        logger.debug("Returning: %s", json_response)
        return json_response

    def _build_uri(self, api_call: UnifiAPI) -> str:
        logger.debug("Entering: _build_uri")
        logger.debug("CommonEndpoint: %s", api_call.api_class.common_endpoint)
        uri_string = self.endpoint + api_call.api_class.common_endpoint + api_call.endpoint
        logger.debug("_build_uri returning: %s", uri_string)
        return uri_string

    def _substitute_symbolics(self, initial_uri: str, substitutions: dict[UnifiEndpointSymbolics, str]) -> str:
        logger.debug("Entering: _substitute_symbolics")
        if "{{" not in initial_uri or "}}" not in initial_uri:
            return initial_uri

        result = initial_uri
        for symbolic, value in substitutions.items():
            logger.debug("Processing: %s with %s", symbolic, value)
            result = result.replace(symbolic.symbolic, value)

        logger.debug("Returning: %s", result)
        return result

    @staticmethod
    def _create_command_body(api_call: UnifiAPI, mac_address: str | None) -> str:
        logger.debug("Entering: _create_command_body")
        if mac_address is None:
            body = json.dumps({"cmd": api_call.name})
        else:
            body = json.dumps({"cmd": api_call.name, "mac": mac_address})
        logger.debug("Returning: %s", body)
        return body
