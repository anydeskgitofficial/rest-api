import json, urllib

class ClientId:
    """Represents a client ID and alias."""

    def __init__(self, api, id, alias):
        self.api = api
        self.id = id
        self.alias = alias

    def __str__(self):
        return str(self.alias) + " (" + str(self.id) + ")"

    def client(self):
        """Get client with this id."""
        data = json.loads(self.api.request("clients/" + str(self.id)).decode('utf-8'))
        ver = ""
        online = False
        online_time = -1
        comment = None
        if "client-version" in data: ver = data["client-version"]
        if "online" in data: online = data["online"]
        if "online-time" in data: online_time = data["online-time"]
        if "comment" in data: comment = data["comment"]

        return Client(self.api, data["cid"], data["alias"], ver, online, online_time, comment)

    def last_sessions(self):
        """Get the 5 last sessions of this client"""
        data = json.loads(self.api.request("clients/" + str(self.id)).decode('utf-8'))
        sessions = []
        for session in data["last-sessions"]:
            sessions.append(self.api._session_from_data(session))
        return sessions

    def row(self):
        return [
            self.id,
            self.alias
        ]

    def change_alias(self, alias):
        """Change the alias of the client."""
        try:
            print(self.api.patch("clients/" + str(self.id), json.dumps({"alias": alias})))
            self.alias = alias
        except urllib.error.HTTPError as err:
            if err.code == 400:
                raise AliasException("Invalid alias")
            elif err.code == 409:
                raise AliasException("Requested alias is already in use")
            elif err.code == 403:
                error_data = json.loads(err.read().decode('utf-8'))
                raise AliasException(error_data["code"] + ": " + error_data["error"])
            elif err.code == 402:
                raise AliasException("Namespace reached its maximum size.")
            else:
                raise err

    # Added this function to remove the alias from an ID
    def remove_alias(self):
        """Change the alias of the client."""
        try:
            # Removed the print in the following line
            self.api.patch("clients/" + str(self.id), json.dumps({"alias": None}))
            self.alias = None
        except urllib.error.HTTPError as err:
            if err.code == 400:
                raise AliasException("Invalid alias")
            elif err.code == 409:
                raise AliasException("Requested alias is already in use")
            elif err.code == 403:
                error_data = json.loads(err.read().decode('utf-8'))
                raise AliasException(error_data["code"] + ": " + error_data["error"])
            elif err.code == 402:
                raise AliasException("Namespace reached its maximum size.")
            else:
                raise err

    def change_comment(self, comment):
        """Change the comment of the client."""
        self.api.patch("clients/" + str(self.id), json.dumps({"comment": comment}))
        self.comment = comment

class AliasException(Exception):
    def __init__(self, text):
        super(AliasException, self).__init__(text)

class Client(ClientId):
    def __init__(self, api, id, alias, version, is_online, online_time, comment=None):
        super(Client, self).__init__(api, id, alias)
        self.version = version
        self.is_online = is_online
        self.online_time = online_time
        self.comment = comment

    def row(self):
        return [
            self.id,
            self.alias,
            self.online_time,
            self.version,
            self.comment
        ]
