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

from unifi_utils.api import UnifiAPI
from unifi_utils.enums import HTTPCall, UnifiApiClass, UnifiCommandManager


class TestUnifiAPIProperties:
    def test_status_get_properties(self):
        api = UnifiAPI.StatusGet
        assert api.endpoint == "/status"
        assert api.name == "Status"
        assert api.call_type == HTTPCall.GET
        assert api.api_class == UnifiApiClass.Controller
        assert api.command_manager == UnifiCommandManager.Non
        assert api.requires_site is False

    def test_health_get_requires_site(self):
        api = UnifiAPI.HealthGet
        assert api.requires_site is True
        assert api.api_class == UnifiApiClass.Site

    def test_device_restart_post_is_callable_command(self):
        api = UnifiAPI.DeviceRestartPost
        assert api.api_class == UnifiApiClass.CallableCommand
        assert api.command_manager == UnifiCommandManager.DeviceManager
        assert api.call_type == HTTPCall.POST
        assert api.name == "restart"

    def test_client_block_post_uses_status_manager(self):
        api = UnifiAPI.ClientBlockPost
        assert api.command_manager == UnifiCommandManager.StatusManager
        assert api.name == "block-sta"


class TestUnifiAPIValidation:
    @pytest.mark.parametrize("api", list(UnifiAPI))
    def test_all_endpoints_have_required_properties(self, api):
        assert api.endpoint is not None
        assert api.name is not None
        assert api.call_type is not None
        assert api.api_class is not None
        assert api.command_manager is not None

    @pytest.mark.parametrize("api", list(UnifiAPI))
    def test_all_endpoints_have_valid_paths(self, api):
        endpoint = api.endpoint
        if api.api_class == UnifiApiClass.CallableCommand:
            assert endpoint == "", f"CallableCommand endpoint should be empty for {api}"
        else:
            assert endpoint.startswith("/"), f"Endpoint should start with / for {api}"


class TestUnifiAPICategories:
    def test_controller_apis_do_not_require_site(self):
        assert UnifiAPI.StatusGet.requires_site is False
        assert UnifiAPI.LoginPost.requires_site is False
        assert UnifiAPI.LogoutPost.requires_site is False
        assert UnifiAPI.SelfGet.requires_site is False

    def test_site_apis_require_site(self):
        assert UnifiAPI.HealthGet.requires_site is True
        assert UnifiAPI.ActiveClientsGet.requires_site is True
        assert UnifiAPI.DevicesGet.requires_site is True
        assert UnifiAPI.WlanConfGet.requires_site is True

    def test_get_endpoints_have_get_call_type(self):
        assert UnifiAPI.StatusGet.call_type == HTTPCall.GET
        assert UnifiAPI.HealthGet.call_type == HTTPCall.GET
        assert UnifiAPI.ActiveClientsGet.call_type == HTTPCall.GET
        assert UnifiAPI.DevicesGet.call_type == HTTPCall.GET

    def test_post_endpoints_have_post_call_type(self):
        assert UnifiAPI.LoginPost.call_type == HTTPCall.POST
        assert UnifiAPI.DeviceRestartPost.call_type == HTTPCall.POST
        assert UnifiAPI.ClientBlockPost.call_type == HTTPCall.POST

    def test_put_endpoints_have_put_call_type(self):
        assert UnifiAPI.ClientUpdatePut.call_type == HTTPCall.PUT
        assert UnifiAPI.DeviceUpdatePut.call_type == HTTPCall.PUT
