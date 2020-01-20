class License:
    def __init__(self, api, name, expires, max_clients, max_sessions, max_session_time, license_id, license_key, api_password, namespaces):
        self.api = api
        self.name = name
        self.expires = expires
        self.max_clients = max_clients
        self.max_sessions = max_sessions
        self.max_session_time = max_session_time
        self.license_id = license_id
        self.license_key = license_key
        self.api_password = api_password
        self.namespaces = namespaces

class SysInfo:
    def __init__(self, api, name, version, client_count, online_count, session_count, active_session_count, standalone, license):
        self.api = api
        self.name = name
        self.version = version
        self.client_count = client_count
        self.online_count = online_count
        self.session_count = session_count
        self.active_session_count = active_session_count
        self.standalone = standalone
        self.license = license

class Namespace:
    def __init__(self, api, name, size):
        self.api = api
        self.name = name
        self.size = size

    def __str__(self):
        return self.name
