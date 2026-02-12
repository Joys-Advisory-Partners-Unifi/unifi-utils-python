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

import pytest
import responses

from unifi_utils.api import UnifiAPI
from unifi_utils.client import UnifiUtils
from unifi_utils.enums import UnifiEndpointSymbolics

TEST_API_KEY = "test-api-key-12345"
TEST_SITE = "default"
TEST_ENDPOINT = "http://localhost:8443"


@pytest.fixture
def client():
    return UnifiUtils(TEST_ENDPOINT, TEST_API_KEY, TEST_SITE)


class TestConstructor:
    def test_initialization(self):
        utils = UnifiUtils("https://example.com", "api-key", "mysite")
        assert utils.endpoint == "https://example.com"
        assert utils.api_key == "api-key"
        assert utils.site == "mysite"

    def test_session_initialized(self):
        utils = UnifiUtils("https://example.com", "api-key", "mysite")
        assert utils.session is not None

    def test_session_headers(self):
        utils = UnifiUtils("https://example.com", "api-key", "mysite")
        assert utils.session.headers["X-API-KEY"] == "api-key"
        assert utils.session.headers["Accept"] == "application/json"
        assert utils.session.headers["Content-Type"] == "application/json"


class TestMakeAPICallGET:
    @responses.activate
    def test_status_get(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": {"status": "ok"}}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/status",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.StatusGet)

        assert result is not None
        assert "meta" in result
        assert result["meta"]["rc"] == "ok"

    @responses.activate
    def test_health_get_with_site_substitution(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": []}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/stat/health",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.HealthGet)

        assert result is not None
        assert "meta" in result

    @responses.activate
    def test_active_clients_get(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": [{"mac": "aa:bb:cc:dd:ee:ff", "hostname": "device1"}]}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/stat/sta",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.ActiveClientsGet)

        assert result is not None
        assert "data" in result
        assert len(result["data"]) == 1

    @responses.activate
    def test_devices_get(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": [{"mac": "11:22:33:44:55:66", "model": "UAP-AC-Pro"}]}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/stat/device",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.DevicesGet)

        assert result is not None
        assert "data" in result


class TestMakeAPICallPOST:
    @responses.activate
    def test_login_post_with_body(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": []}
        responses.add(
            responses.POST,
            f"{TEST_ENDPOINT}/proxy/network/api/login",
            json=json_response,
            status=200,
        )

        body = {"username": "admin", "password": "password"}
        result = client.make_api_call(UnifiAPI.LoginPost, json_body=body)

        assert result is not None
        assert "meta" in result
        # Verify the request body was sent
        sent_body = json.loads(responses.calls[0].request.body)
        assert sent_body["username"] == "admin"

    @responses.activate
    def test_device_restart_with_mac_address(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": []}
        mac_address = "aa:bb:cc:dd:ee:ff"
        responses.add(
            responses.POST,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/cmd/devmgr",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.DeviceRestartPost, mac_address=mac_address)

        assert result is not None
        assert "meta" in result
        # Verify command body includes mac
        sent_body = json.loads(responses.calls[0].request.body)
        assert sent_body["cmd"] == "restart"
        assert sent_body["mac"] == mac_address

    @responses.activate
    def test_callable_command_without_mac(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": []}
        responses.add(
            responses.POST,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/cmd/backup",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.BackupCreatePost)

        assert result is not None
        sent_body = json.loads(responses.calls[0].request.body)
        assert sent_body["cmd"] == "backup"


class TestMakeAPICallPUT:
    @responses.activate
    def test_client_update_put(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": []}
        responses.add(
            responses.PUT,
            f"{TEST_ENDPOINT}/proxy/network/api/s/{TEST_SITE}/rest/user",
            json=json_response,
            status=200,
        )

        body = {"name": "Updated Client"}
        result = client.make_api_call(UnifiAPI.ClientUpdatePut, json_body=body)

        assert result is not None
        assert "meta" in result


class TestAPIKeyHeader:
    @responses.activate
    def test_api_key_header_included(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": {}}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/status",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.StatusGet)

        assert result is not None
        assert responses.calls[0].request.headers["X-API-KEY"] == TEST_API_KEY


class TestJSONParsing:
    @responses.activate
    def test_json_response_with_data_array(self, client):
        json_response = {"meta": {"rc": "ok"}, "data": [{"name": "test", "value": 123}]}
        responses.add(
            responses.GET,
            f"{TEST_ENDPOINT}/proxy/network/status",
            json=json_response,
            status=200,
        )

        result = client.make_api_call(UnifiAPI.StatusGet)

        assert result is not None
        assert "meta" in result
        assert "data" in result
        assert result["meta"]["rc"] == "ok"
        assert isinstance(result["data"], list)
        assert len(result["data"]) == 1


class TestURLConstruction:
    def test_build_uri_controller(self, client):
        uri = client._build_uri(UnifiAPI.StatusGet)
        assert uri == f"{TEST_ENDPOINT}/proxy/network/status"

    def test_build_uri_site(self, client):
        uri = client._build_uri(UnifiAPI.HealthGet)
        assert uri == f"{TEST_ENDPOINT}/proxy/network/api/s/{{{{site}}}}/stat/health"

    def test_substitute_symbolics_site(self, client):
        uri = f"{TEST_ENDPOINT}/proxy/network/api/s/{{{{site}}}}/stat/health"
        result = client._substitute_symbolics(uri, {UnifiEndpointSymbolics.Site: "default"})
        assert result == f"{TEST_ENDPOINT}/proxy/network/api/s/default/stat/health"

    def test_substitute_symbolics_no_symbolics(self, client):
        uri = f"{TEST_ENDPOINT}/proxy/network/status"
        result = client._substitute_symbolics(uri, {})
        assert result == uri

    def test_substitute_symbolics_multiple(self, client):
        uri = f"{TEST_ENDPOINT}/proxy/network/api/s/{{{{site}}}}/cmd/{{{{manager}}}}"
        result = client._substitute_symbolics(uri, {
            UnifiEndpointSymbolics.Site: "mysite",
            UnifiEndpointSymbolics.Manager: "devmgr",
        })
        assert result == f"{TEST_ENDPOINT}/proxy/network/api/s/mysite/cmd/devmgr"


class TestCreateCommandBody:
    def test_command_body_without_mac(self):
        body = UnifiUtils._create_command_body(UnifiAPI.DeviceRestartPost, None)
        parsed = json.loads(body)
        assert parsed["cmd"] == "restart"
        assert "mac" not in parsed

    def test_command_body_with_mac(self):
        body = UnifiUtils._create_command_body(UnifiAPI.DeviceRestartPost, "aa:bb:cc:dd:ee:ff")
        parsed = json.loads(body)
        assert parsed["cmd"] == "restart"
        assert parsed["mac"] == "aa:bb:cc:dd:ee:ff"
