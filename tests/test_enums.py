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

import pytest

from unifi_utils.enums import (
    HTTPCall,
    UnifiApiClass,
    UnifiCommandManager,
    UnifiEndpointSymbolics,
)


class TestHTTPCall:
    def test_get(self):
        assert HTTPCall.GET.value == "GET"

    def test_put(self):
        assert HTTPCall.PUT.value == "PUT"

    def test_post(self):
        assert HTTPCall.POST.value == "POST"

    def test_delete(self):
        assert HTTPCall.DELETE.value == "DELETE"

    def test_head(self):
        assert HTTPCall.HEAD.value == "HEAD"


class TestUnifiApiClass:
    def test_controller_common_endpoint(self):
        assert UnifiApiClass.Controller.common_endpoint == "/proxy/network"

    def test_site_common_endpoint(self):
        assert UnifiApiClass.Site.common_endpoint == "/proxy/network/api/s/{{site}}"

    def test_callable_command_common_endpoint(self):
        assert UnifiApiClass.CallableCommand.common_endpoint == "/proxy/network/api/s/{{site}}/cmd/{{manager}}"

    def test_all_classes_have_common_endpoint(self):
        for api_class in UnifiApiClass:
            if api_class.name.startswith("_"):
                continue
            assert api_class.common_endpoint is not None


class TestUnifiCommandManager:
    def test_device_manager(self):
        assert UnifiCommandManager.DeviceManager.manager == "devmgr"

    def test_status_manager(self):
        assert UnifiCommandManager.StatusManager.manager == "stamgr"

    def test_site_management(self):
        assert UnifiCommandManager.SiteManagement.manager == "sitemgr"

    def test_event_management(self):
        assert UnifiCommandManager.EventManagement.manager == "evtmgt"

    def test_backup(self):
        assert UnifiCommandManager.Backup.manager == "backup"

    def test_system(self):
        assert UnifiCommandManager.System.manager == "system"

    def test_stat(self):
        assert UnifiCommandManager.Stat.manager == "stat"

    def test_none_manager(self):
        manager = UnifiCommandManager.Non.manager
        assert manager is None

    def test_all_managers_accessible(self):
        for mgr in UnifiCommandManager:
            # Should not raise
            _ = mgr.manager


class TestUnifiEndpointSymbolics:
    def test_site(self):
        assert UnifiEndpointSymbolics.Site.symbolic == "{{site}}"

    def test_mac(self):
        assert UnifiEndpointSymbolics.Mac.symbolic == "{{mac}}"

    def test_id(self):
        assert UnifiEndpointSymbolics.ID.symbolic == "{{_id}}"

    def test_manager(self):
        assert UnifiEndpointSymbolics.Manager.symbolic == "{{manager}}"

    def test_interval(self):
        assert UnifiEndpointSymbolics.Interval.symbolic == "{{interval}}"

    def test_type(self):
        assert UnifiEndpointSymbolics.Type.symbolic == "{{type}}"
