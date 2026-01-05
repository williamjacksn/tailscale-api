import datetime
import ipaddress
from typing import TypedDict

type IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address


class DeviceDict(TypedDict):
    addresses: list[str]
    authorized: bool
    blocksIncomingConnections: bool
    clientVersion: str
    connectedToControl: bool
    created: str
    expires: str
    hostname: str
    id: str
    isExternal: bool
    keyExpiryDisabled: bool
    lastSeen: str
    machineKey: str
    name: str
    nodeId: str
    nodeKey: str
    os: str
    tailnetLockError: str
    tailnetLockKey: str
    updateAvailable: bool
    user: str


class Device:
    def __init__(self, data: DeviceDict) -> None:
        self.data = data

    @property
    def addresses(self) -> list[IPAddress]:
        return [ipaddress.ip_address(i) for i in self.data.get("addresses", [])]

    @property
    def authorized(self) -> bool:
        return self.data.get("authorized")

    @property
    def blocks_incoming_connections(self) -> bool:
        return self.data.get("blocksIncomingConnections")

    @property
    def client_version(self) -> str:
        return self.data.get("clientVersion")

    @property
    def connected_to_control(self) -> bool:
        return self.data.get("connectedToControl")

    @property
    def created(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.data.get("created"))

    @property
    def expires(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.data.get("expires"))

    @property
    def hostname(self) -> str:
        return self.data.get("hostname")

    @property
    def id(self) -> str:
        return self.data.get("id")

    @property
    def is_external(self) -> bool:
        return self.data.get("isExternal")

    @property
    def key_expiry_disabled(self) -> bool:
        return self.data.get("keyExpiryDisabled")

    @property
    def last_seen(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.data.get("lastSeen"))

    @property
    def machine_key(self) -> str:
        return self.data.get("machineKey")

    @property
    def name(self) -> str:
        return self.data.get("name")

    @property
    def node_id(self) -> str:
        return self.data.get("nodeId")

    @property
    def node_key(self) -> str:
        return self.data.get("nodeKey")

    @property
    def os(self) -> str:
        return self.data.get("os")

    @property
    def tailnet_lock_error(self) -> str:
        return self.data.get("tailnetLockError")

    @property
    def tailnet_lock_key(self) -> str:
        return self.data.get("tailnetLockKey")

    @property
    def update_available(self) -> bool:
        return self.data.get("updateAvailable")

    @property
    def user(self) -> str:
        return self.data.get("user")
