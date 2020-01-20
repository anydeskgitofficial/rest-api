import urllib.request
import hashlib, hmac, base64
import time, json
import configparser

from .session import *
from .addressbook import *
from .client import *
from .sysinfo import *

class API:
    def __init__(self, license="", key="", url="https://v1.api.anydesk.com:8081/", path=""):
        self.url = url
        if path != "":
            config = configparser.ConfigParser()
            config.read(path)
            self.license = config["Auth"]["license"]
            self.key = config["Auth"]["key"]
        else:
            self.license = license
            self.key = key

    def auth(self, resource, content="", method="GET"):
        sha1 = hashlib.sha1()
        sha1.update(content.encode("utf8"))
        content_hash = str(base64.b64encode(sha1.digest()), "UTF-8")
        timestamp = str(int(time.time()))
        request_string = method + "\n" + resource + "\n" + timestamp + "\n" + content_hash
        token = str(base64.b64encode(hmac.new(
                self.key.encode("utf-8"),
                request_string.encode("utf-8"),
                hashlib.sha1
            ).digest()),
            "UTF-8"
        )
        return "AD " + self.license + ":" + timestamp + ":" + token

    def request(self, resource):
        req = urllib.request.Request(self.url + resource, headers={
            "Authorization": self.auth("/" + resource)
        })
        res = urllib.request.urlopen(req)
        return res.read()
	
    def put(self, resource, body):
        req = urllib.request.Request(self.url + resource, body.encode("utf-8"), headers={
            "Authorization": self.auth("/" + resource, content=body, method="PUT"),
            "Content-Type": "application/json"
        })
        req.get_method = lambda: "PUT"
        res = urllib.request.urlopen(req)
        return res.read()

    def delete(self, resource, body):
        req = urllib.request.Request(self.url + resource, body.encode("utf-8"), headers={
            "Authorization": self.auth("/" + resource, content=body, method="DELETE"),
            "Content-Type": "application/json"
        })
        req.get_method = lambda: "DELETE"
        res = urllib.request.urlopen(req)
        return res.read()

    def patch(self, resource, body):
        req = urllib.request.Request(self.url + resource, body.encode("utf-8"), headers={
            "Authorization": self.auth("/" + resource, content=body, method="PATCH"),
            "Content-Type": "application/json"
        })
        req.get_method = lambda: "PATCH"
        res = urllib.request.urlopen(req)
        return res.read()


    def post(self, resource, body):
        req = urllib.request.Request(self.url + resource, body.encode("utf-8"), headers={
            "Authorization": self.auth("/" + resource, content=body, method="POST"),
            "Content-Type": "application/json"
        })
        res = urllib.request.urlopen(req)
        return res.read()

    def _client_from_data(self, client):
        comment = None
        if "comment" in client: comment = client["comment"]
        return Client(
            self,
            client["cid"],
            client["alias"],
            client["client-version"],
            client["online"],
            client["online-time"],
            comment
        )

    def all_clients(self):
        """Download a list of all clients."""
        data = json.loads(self.request("clients").decode('utf-8'))
        clients = []
        for client in data["list"]:
            clients.append(self._client_from_data(client))
        return clients

    def _session_from_data(self, session):
        return Session(
            self,
            session["sid"],
            ClientId(
                self,
                session["from"]["cid"],
                session["from"]["alias"]
            ),
            ClientId(
                self,
                session["to"]["cid"],
                session["to"]["alias"]
            ),
            session["active"],
            session["start-time"],
            session["end-time"],
            session["duration"],
            session["comment"]
        )

    def all_sessions(self, client=None):
        """Downlaod a list of all sessions."""

        if client != None:
            data = json.loads(self.request("sessions?cid=" + str(client.id)).decode('utf-8'))
        else:
            data = json.loads(self.request("sessions").decode('utf-8'))

        sessions = []
        for session in data["list"]:
            sessions.append(self._session_from_data(session))
            print(str(session))
        return sessions

    def query_sessions(self, **params):
        """
        List sessions according to given parameters.

        direction - in/out/inout - List only incoming or outgoing sessions
        start - Only list sessions after the given Unix-Timestamp
        end - Only list sessions before the given Unix-Timestamp
        sort - from.cid/to.cid/start-time/end-time/duration - Sort list by given parameter
        offset - Index of the first item listed
        limit - Maximum number of items listed
        """

        param_strs = []
        for key in params:
            if key == "start":
                param_strs.append("from=" + str(params[key]))
            elif key == "end":
                param_strs.append("to=" + str(params[key]))
            else:
                param_strs.append(key + "=" + str(params[key]))

        resource = "sessions?" + "&".join(param_strs)
        if len(param_strs) == 0: resource = "sessions"
        data = json.loads(self.request(resource).decode('utf-8'))
        sessions = []
        for session in data["list"]:
            sessions.append(self._session_from_data(session))
        return sessions

    def query_clients(self, **params):
        """
        List sessions according to given parameters.

        online - True - Only list online clients
        filter - Filter by given parameter
        sort - cid/alias/online - Sort list by given parameter
        offset - Index of the first item listed
        limit - Maximum number of items listed
        """
        param_strs = []
        for key in params:
            if type(params[key]) == bool and params[key] == True:
                param_strs.append(key)
            else:
                param_strs.append(key + "=" + str(params[key]))

        resource = "clients?" + "&".join(param_strs)
        if len(param_strs) == 0: resource = "clients"
        data = json.loads(self.request(resource).decode('utf-8'))
        clients = []
        for client in data["list"]:
            clients.append(self._client_from_data(client))
        return clients

    def all_addressbooks(self):
        """Download a list of all addressbooks."""
        data = json.loads(self.request("rosters").decode('utf-8'))
        addressbooks = []
        for addressbook in data["list"]:
            addressbooks.append(Addressbook(
                self,
                addressbook["roster_id"],
                addressbook["name"]
            ))
        return addressbooks

    def sysinfo(self):
        """Get system information."""
        data = json.loads(self.request("sysinfo").decode('utf-8'))

        namespaces = []
        for namespace in data["license"]["namespaces"]:
            namespaces.append(Namespace(self, namespace["name"], namespace["size"]))

        return SysInfo(
            self,
            data["name"],
            data["api-ver"],
            data["clients"]["total"],
            data["clients"]["online"],
            data["sessions"]["total"],
            data["sessions"]["active"],
            data["standalone"],
            License(
                self,
                data["license"]["name"],
                data["license"]["expires"],
                data["license"]["max-clients"],
                data["license"]["max-sessions"],
                data["license"]["max-session-time"],
                data["license"]["license-id"],
                data["license"]["license-key"],
                data["license"]["api-password"],
                namespaces
            )
        )
