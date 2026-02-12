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
from typing import NamedTuple

from .enums import HTTPCall, UnifiApiClass, UnifiCommandManager


class _APIDef(NamedTuple):
    endpoint: str
    requires_site: bool
    call_type: HTTPCall
    name: str
    api_class: UnifiApiClass
    command_manager: UnifiCommandManager


class UnifiAPI(Enum):
    # ==========================================
    # Controller APIs (no site required)
    # ==========================================

    # Authentication
    StatusGet = _APIDef("/status", False, HTTPCall.GET, "Status", UnifiApiClass.Controller, UnifiCommandManager.Non)
    LoginPost = _APIDef("/api/login", False, HTTPCall.POST, "Login", UnifiApiClass.Controller, UnifiCommandManager.Non)
    LogoutPost = _APIDef("/api/logout", False, HTTPCall.POST, "Logout", UnifiApiClass.Controller, UnifiCommandManager.Non)

    # User Information
    SelfGet = _APIDef("/api/self", False, HTTPCall.GET, "Self", UnifiApiClass.Controller, UnifiCommandManager.Non)
    SelfSitesGet = _APIDef("/api/self/sites", False, HTTPCall.GET, "SelfSites", UnifiApiClass.Controller, UnifiCommandManager.Non)

    # Controller Statistics
    StatSitesGet = _APIDef("/api/stat/sites", False, HTTPCall.GET, "StatSites", UnifiApiClass.Controller, UnifiCommandManager.Non)
    StatAdminGet = _APIDef("/api/stat/admin", False, HTTPCall.GET, "StatAdmin", UnifiApiClass.Controller, UnifiCommandManager.Non)

    # System Management
    PowerOffPost = _APIDef("/api/system/poweroff", False, HTTPCall.POST, "PowerOff", UnifiApiClass.Controller, UnifiCommandManager.Non)
    PowerRebootPost = _APIDef("/api/system/reboot", False, HTTPCall.POST, "Reboot", UnifiApiClass.Controller, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Health & Status
    # ==========================================
    HealthGet = _APIDef("/stat/health", True, HTTPCall.GET, "Health", UnifiApiClass.Site, UnifiCommandManager.Non)
    SiteSelfGet = _APIDef("/self", True, HTTPCall.GET, "SiteSelf", UnifiApiClass.Site, UnifiCommandManager.Non)
    SysInfoGet = _APIDef("/stat/sysinfo", True, HTTPCall.GET, "SysInfo", UnifiApiClass.Site, UnifiCommandManager.Non)
    CountryCodesGet = _APIDef("/stat/ccode", True, HTTPCall.GET, "CountryCodes", UnifiApiClass.Site, UnifiCommandManager.Non)
    CurrentChannelsGet = _APIDef("/stat/current-channel", True, HTTPCall.GET, "CurrentChannels", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Events & Alarms
    # ==========================================
    EventsGet = _APIDef("/stat/event", True, HTTPCall.GET, "Events", UnifiApiClass.Site, UnifiCommandManager.Non)
    OldestEventsGet = _APIDef("/rest/event", True, HTTPCall.GET, "OldestEvents", UnifiApiClass.Site, UnifiCommandManager.Non)
    AlarmsGet = _APIDef("/stat/alarm", True, HTTPCall.GET, "Alarms", UnifiApiClass.Site, UnifiCommandManager.Non)
    OldestAlarmsGet = _APIDef("/rest/alarm", True, HTTPCall.GET, "OldestAlarms", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Client Management
    # ==========================================
    ActiveClientsGet = _APIDef("/stat/sta", True, HTTPCall.GET, "ActiveClients", UnifiApiClass.Site, UnifiCommandManager.Non)
    AllClientsGet = _APIDef("/rest/user", True, HTTPCall.GET, "AllClients", UnifiApiClass.Site, UnifiCommandManager.Non)
    ClientCreatePost = _APIDef("/rest/user", True, HTTPCall.POST, "ClientCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    ClientUpdatePut = _APIDef("/rest/user", True, HTTPCall.PUT, "ClientUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    ClientModifyPut = _APIDef("/upd/user/{{_id}}", True, HTTPCall.PUT, "ClientModify", UnifiApiClass.Site, UnifiCommandManager.Non)

    # Client Commands (via stamgr)
    ClientBlockPost = _APIDef("", True, HTTPCall.POST, "block-sta", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    ClientUnblockPost = _APIDef("", True, HTTPCall.POST, "unblock-sta", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    ClientKickPost = _APIDef("", True, HTTPCall.POST, "kick-sta", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    ClientForgetPost = _APIDef("", True, HTTPCall.POST, "forget-sta", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    ClientUnauthorizeGuestPost = _APIDef("", True, HTTPCall.POST, "unauthorize-guest", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    ClientAuthorizeGuestPost = _APIDef("", True, HTTPCall.POST, "authorize-guest", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)

    # ==========================================
    # Site APIs - VPN
    # ==========================================
    RemoteUserVpnGet = _APIDef("/stat/remoteuservpn", True, HTTPCall.GET, "RemoteUserVpn", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Device Management
    # ==========================================
    DevicesBasicGet = _APIDef("/stat/device-basic", True, HTTPCall.GET, "DevicesBasic", UnifiApiClass.Site, UnifiCommandManager.Non)
    DevicesGet = _APIDef("/stat/device", True, HTTPCall.GET, "Devices", UnifiApiClass.Site, UnifiCommandManager.Non)
    DeviceGet = _APIDef("/stat/device/{{mac}}", True, HTTPCall.GET, "Device", UnifiApiClass.Site, UnifiCommandManager.Non)
    DevicesFilteredPost = _APIDef("/stat/device", True, HTTPCall.POST, "DevicesFiltered", UnifiApiClass.Site, UnifiCommandManager.Non)
    DeviceUpdatePut = _APIDef("/rest/device/{{_id}}", True, HTTPCall.PUT, "DeviceUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)

    # Device Commands (via devmgr)
    DeviceAdoptPost = _APIDef("", True, HTTPCall.POST, "adopt", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceRestartPost = _APIDef("", True, HTTPCall.POST, "restart", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceForceProvisionPost = _APIDef("", True, HTTPCall.POST, "force-provision", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DevicePowerCyclePost = _APIDef("", True, HTTPCall.POST, "power-cycle", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceSpeedTestPost = _APIDef("", True, HTTPCall.POST, "speedtest", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceSpeedTestStatusPost = _APIDef("", True, HTTPCall.POST, "speedtest-status", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceLocateEnablePost = _APIDef("", True, HTTPCall.POST, "set-locate", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceLocateDisablePost = _APIDef("", True, HTTPCall.POST, "unset-locate", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceUpgradePost = _APIDef("", True, HTTPCall.POST, "upgrade", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceMigratePost = _APIDef("", True, HTTPCall.POST, "migrate", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)
    DeviceSpectrumScanPost = _APIDef("", True, HTTPCall.POST, "spectrum-scan", UnifiApiClass.CallableCommand, UnifiCommandManager.DeviceManager)

    # ==========================================
    # Site APIs - Network Configuration
    # ==========================================
    NetworkConfGet = _APIDef("/rest/networkconf", True, HTTPCall.GET, "NetworkConf", UnifiApiClass.Site, UnifiCommandManager.Non)
    NetworkConfCreatePost = _APIDef("/rest/networkconf", True, HTTPCall.POST, "NetworkConfCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    NetworkConfUpdatePut = _APIDef("/rest/networkconf/{{_id}}", True, HTTPCall.PUT, "NetworkConfUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    NetworkConfDeleteDelete = _APIDef("/rest/networkconf/{{_id}}", True, HTTPCall.DELETE, "NetworkConfDelete", UnifiApiClass.Site, UnifiCommandManager.Non)
    RoutingActiveGet = _APIDef("/stat/routing", True, HTTPCall.GET, "RoutingActive", UnifiApiClass.Site, UnifiCommandManager.Non)
    RoutingGet = _APIDef("/rest/routing", True, HTTPCall.GET, "Routing", UnifiApiClass.Site, UnifiCommandManager.Non)
    RoutingCreatePost = _APIDef("/rest/routing", True, HTTPCall.POST, "RoutingCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RoutingUpdatePut = _APIDef("/rest/routing/{{_id}}", True, HTTPCall.PUT, "RoutingUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RoutingDeleteDelete = _APIDef("/rest/routing/{{_id}}", True, HTTPCall.DELETE, "RoutingDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Firewall Configuration
    # ==========================================
    FirewallRulesGet = _APIDef("/rest/firewallrule", True, HTTPCall.GET, "FirewallRules", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallRuleCreatePost = _APIDef("/rest/firewallrule", True, HTTPCall.POST, "FirewallRuleCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallRuleUpdatePut = _APIDef("/rest/firewallrule/{{_id}}", True, HTTPCall.PUT, "FirewallRuleUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallRuleDeleteDelete = _APIDef("/rest/firewallrule/{{_id}}", True, HTTPCall.DELETE, "FirewallRuleDelete", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallGroupsGet = _APIDef("/rest/firewallgroup", True, HTTPCall.GET, "FirewallGroups", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallGroupCreatePost = _APIDef("/rest/firewallgroup", True, HTTPCall.POST, "FirewallGroupCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallGroupUpdatePut = _APIDef("/rest/firewallgroup/{{_id}}", True, HTTPCall.PUT, "FirewallGroupUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    FirewallGroupDeleteDelete = _APIDef("/rest/firewallgroup/{{_id}}", True, HTTPCall.DELETE, "FirewallGroupDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Port Forwarding
    # ==========================================
    PortForwardsGet = _APIDef("/stat/portforward", True, HTTPCall.GET, "PortForwards", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortForwardCreatePost = _APIDef("/rest/portforward", True, HTTPCall.POST, "PortForwardCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortForwardUpdatePut = _APIDef("/rest/portforward/{{_id}}", True, HTTPCall.PUT, "PortForwardUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortForwardDeleteDelete = _APIDef("/rest/portforward/{{_id}}", True, HTTPCall.DELETE, "PortForwardDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - WLAN Configuration
    # ==========================================
    WlanConfGet = _APIDef("/rest/wlanconf", True, HTTPCall.GET, "WlanConf", UnifiApiClass.Site, UnifiCommandManager.Non)
    WlanConfCreatePost = _APIDef("/rest/wlanconf", True, HTTPCall.POST, "WlanConfCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    WlanConfDetailGet = _APIDef("/rest/wlanconf/{{_id}}", True, HTTPCall.GET, "WlanConfDetail", UnifiApiClass.Site, UnifiCommandManager.Non)
    WlanConfUpdatePut = _APIDef("/rest/wlanconf/{{_id}}", True, HTTPCall.PUT, "WlanConfUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    WlanConfDeleteDelete = _APIDef("/rest/wlanconf/{{_id}}", True, HTTPCall.DELETE, "WlanConfDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Site Settings
    # ==========================================
    SettingsGet = _APIDef("/rest/setting", True, HTTPCall.GET, "Settings", UnifiApiClass.Site, UnifiCommandManager.Non)
    SettingUpdatePut = _APIDef("/rest/setting/{{key}}/{{_id}}", True, HTTPCall.PUT, "SettingUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - DPI & Analytics
    # ==========================================
    SiteDpiGet = _APIDef("/stat/sitedpi", True, HTTPCall.GET, "SiteDpi", UnifiApiClass.Site, UnifiCommandManager.Non)
    SiteDpiPost = _APIDef("/stat/sitedpi", True, HTTPCall.POST, "SiteDpiFiltered", UnifiApiClass.Site, UnifiCommandManager.Non)
    ClientDpiGet = _APIDef("/stat/stadpi", True, HTTPCall.GET, "ClientDpi", UnifiApiClass.Site, UnifiCommandManager.Non)
    ClientDpiPost = _APIDef("/stat/stadpi", True, HTTPCall.POST, "ClientDpiFiltered", UnifiApiClass.Site, UnifiCommandManager.Non)

    # Reports (interval: 5minutes, hourly, daily; type: site, user, ap)
    ReportPost = _APIDef("/stat/report/{{interval}}.{{type}}", True, HTTPCall.POST, "Report", UnifiApiClass.Site, UnifiCommandManager.Non)

    # DPI Commands (via stat manager)
    DpiClearPost = _APIDef("", True, HTTPCall.POST, "clear-dpi", UnifiApiClass.CallableCommand, UnifiCommandManager.Stat)

    # ==========================================
    # Site APIs - RADIUS
    # ==========================================
    RadiusProfilesGet = _APIDef("/rest/radiusprofile", True, HTTPCall.GET, "RadiusProfiles", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusProfileCreatePost = _APIDef("/rest/radiusprofile", True, HTTPCall.POST, "RadiusProfileCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusProfileUpdatePut = _APIDef("/rest/radiusprofile/{{_id}}", True, HTTPCall.PUT, "RadiusProfileUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusProfileDeleteDelete = _APIDef("/rest/radiusprofile/{{_id}}", True, HTTPCall.DELETE, "RadiusProfileDelete", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusAccountsGet = _APIDef("/rest/account", True, HTTPCall.GET, "RadiusAccounts", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusAccountCreatePost = _APIDef("/rest/account", True, HTTPCall.POST, "RadiusAccountCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusAccountUpdatePut = _APIDef("/rest/account/{{_id}}", True, HTTPCall.PUT, "RadiusAccountUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    RadiusAccountDeleteDelete = _APIDef("/rest/account/{{_id}}", True, HTTPCall.DELETE, "RadiusAccountDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Dynamic DNS
    # ==========================================
    DynamicDnsStatusGet = _APIDef("/stat/dynamicdns", True, HTTPCall.GET, "DynamicDnsStatus", UnifiApiClass.Site, UnifiCommandManager.Non)
    DynamicDnsGet = _APIDef("/rest/dynamicdns", True, HTTPCall.GET, "DynamicDns", UnifiApiClass.Site, UnifiCommandManager.Non)
    DynamicDnsUpdatePut = _APIDef("/rest/dynamicdns/{{_id}}", True, HTTPCall.PUT, "DynamicDnsUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Switch Port Profiles
    # ==========================================
    PortProfilesGet = _APIDef("/rest/portconf", True, HTTPCall.GET, "PortProfiles", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortProfileCreatePost = _APIDef("/rest/portconf", True, HTTPCall.POST, "PortProfileCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortProfileUpdatePut = _APIDef("/rest/portconf/{{_id}}", True, HTTPCall.PUT, "PortProfileUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    PortProfileDeleteDelete = _APIDef("/rest/portconf/{{_id}}", True, HTTPCall.DELETE, "PortProfileDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Rogue APs / Neighboring APs
    # ==========================================
    RogueApsGet = _APIDef("/stat/rogueap", True, HTTPCall.GET, "RogueAps", UnifiApiClass.Site, UnifiCommandManager.Non)
    RogueApsPost = _APIDef("/stat/rogueap", True, HTTPCall.POST, "RogueApsFiltered", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Hotspot / Vouchers / Guests
    # ==========================================
    VouchersGet = _APIDef("/stat/voucher", True, HTTPCall.GET, "Vouchers", UnifiApiClass.Site, UnifiCommandManager.Non)
    VoucherCreatePost = _APIDef("", True, HTTPCall.POST, "create-voucher", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    VoucherRevokePost = _APIDef("", True, HTTPCall.POST, "delete-voucher", UnifiApiClass.CallableCommand, UnifiCommandManager.StatusManager)
    GuestsGet = _APIDef("/stat/guest", True, HTTPCall.GET, "Guests", UnifiApiClass.Site, UnifiCommandManager.Non)
    PaymentsGet = _APIDef("/stat/payment", True, HTTPCall.GET, "Payments", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Hotspot Operators
    # ==========================================
    HotspotOperatorsGet = _APIDef("/rest/hotspotop", True, HTTPCall.GET, "HotspotOperators", UnifiApiClass.Site, UnifiCommandManager.Non)
    HotspotOperatorCreatePost = _APIDef("/rest/hotspotop", True, HTTPCall.POST, "HotspotOperatorCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    HotspotOperatorUpdatePut = _APIDef("/rest/hotspotop/{{_id}}", True, HTTPCall.PUT, "HotspotOperatorUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    HotspotOperatorDeleteDelete = _APIDef("/rest/hotspotop/{{_id}}", True, HTTPCall.DELETE, "HotspotOperatorDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - User Groups
    # ==========================================
    UserGroupsGet = _APIDef("/rest/usergroup", True, HTTPCall.GET, "UserGroups", UnifiApiClass.Site, UnifiCommandManager.Non)
    UserGroupCreatePost = _APIDef("/rest/usergroup", True, HTTPCall.POST, "UserGroupCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    UserGroupUpdatePut = _APIDef("/rest/usergroup/{{_id}}", True, HTTPCall.PUT, "UserGroupUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    UserGroupDeleteDelete = _APIDef("/rest/usergroup/{{_id}}", True, HTTPCall.DELETE, "UserGroupDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Media Streaming
    # ==========================================
    MediaFilesGet = _APIDef("/rest/mediafile", True, HTTPCall.GET, "MediaFiles", UnifiApiClass.Site, UnifiCommandManager.Non)
    StreamingGet = _APIDef("/stat/streaming", True, HTTPCall.GET, "Streaming", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Backup Commands (via backup manager)
    # ==========================================
    BackupCreatePost = _APIDef("", True, HTTPCall.POST, "backup", UnifiApiClass.CallableCommand, UnifiCommandManager.Backup)
    BackupListPost = _APIDef("", True, HTTPCall.POST, "list-backups", UnifiApiClass.CallableCommand, UnifiCommandManager.Backup)
    BackupDeletePost = _APIDef("", True, HTTPCall.POST, "delete-backup", UnifiApiClass.CallableCommand, UnifiCommandManager.Backup)

    # ==========================================
    # Site Management Commands (via sitemgr)
    # ==========================================
    GetAdminsPost = _APIDef("", True, HTTPCall.POST, "get-admins", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)
    SiteAddPost = _APIDef("", True, HTTPCall.POST, "add-site", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)
    SiteDeletePost = _APIDef("", True, HTTPCall.POST, "delete-site", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)
    SiteUpdatePost = _APIDef("", True, HTTPCall.POST, "update-site", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)
    DeviceMovePost = _APIDef("", True, HTTPCall.POST, "move-device", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)
    DeviceDeletePost = _APIDef("", True, HTTPCall.POST, "delete-device", UnifiApiClass.CallableCommand, UnifiCommandManager.SiteManagement)

    # ==========================================
    # Event Management Commands (via evtmgt)
    # ==========================================
    EventsArchivePost = _APIDef("", True, HTTPCall.POST, "archive-all-alarms", UnifiApiClass.CallableCommand, UnifiCommandManager.EventManagement)

    # ==========================================
    # Site APIs - SDN / Cloud Access
    # ==========================================
    StatSdnGet = _APIDef("/stat/sdn", True, HTTPCall.GET, "StatSdn", UnifiApiClass.Site, UnifiCommandManager.Non)

    # ==========================================
    # Site APIs - Miscellaneous
    # ==========================================
    TagsGet = _APIDef("/rest/tag", True, HTTPCall.GET, "Tags", UnifiApiClass.Site, UnifiCommandManager.Non)
    TagCreatePost = _APIDef("/rest/tag", True, HTTPCall.POST, "TagCreate", UnifiApiClass.Site, UnifiCommandManager.Non)
    TagUpdatePut = _APIDef("/rest/tag/{{_id}}", True, HTTPCall.PUT, "TagUpdate", UnifiApiClass.Site, UnifiCommandManager.Non)
    TagDeleteDelete = _APIDef("/rest/tag/{{_id}}", True, HTTPCall.DELETE, "TagDelete", UnifiApiClass.Site, UnifiCommandManager.Non)

    # Dashboard & Counters
    CountersGet = _APIDef("/stat/counters", True, HTTPCall.GET, "Counters", UnifiApiClass.Site, UnifiCommandManager.Non)
    DashboardGet = _APIDef("/stat/dashboard", True, HTTPCall.GET, "Dashboard", UnifiApiClass.Site, UnifiCommandManager.Non)

    # WLAN Groups (legacy)
    WlanGroupsGet = _APIDef("/rest/wlangroup", True, HTTPCall.GET, "WlanGroups", UnifiApiClass.Site, UnifiCommandManager.Non)

    @property
    def endpoint(self) -> str:
        return self.value.endpoint

    @property
    def requires_site(self) -> bool:
        return self.value.requires_site

    @property
    def call_type(self) -> HTTPCall:
        return self.value.call_type

    @property
    def name(self) -> str:
        return self.value.name

    @property
    def api_class(self) -> UnifiApiClass:
        return self.value.api_class

    @property
    def command_manager(self) -> UnifiCommandManager:
        return self.value.command_manager
