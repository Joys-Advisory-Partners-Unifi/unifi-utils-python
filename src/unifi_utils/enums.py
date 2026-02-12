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

from enum import Enum


class HTTPCall(Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"
    HEAD = "HEAD"


class UnifiApiClass(Enum):
    Controller = ""
    Site = "/api/s/{{site}}"
    CallableCommand = "/api/s/{{site}}/cmd/{{manager}}"

    _PREFIX = "/proxy/network"

    @property
    def common_endpoint(self) -> str:
        return "/proxy/network" + self.value


class UnifiCommandManager(Enum):
    EventManagement = "evtmgt"
    SiteManagement = "sitemgr"
    StatusManager = "stamgr"
    DeviceManager = "devmgr"
    Backup = "backup"
    System = "system"
    Stat = "stat"
    Non = None

    @property
    def manager(self) -> str | None:
        return self.value


class UnifiEndpointSymbolics(Enum):
    Site = "{{site}}"
    Mac = "{{mac}}"
    ID = "{{_id}}"
    Manager = "{{manager}}"
    Interval = "{{interval}}"
    Type = "{{type}}"

    @property
    def symbolic(self) -> str:
        return self.value
