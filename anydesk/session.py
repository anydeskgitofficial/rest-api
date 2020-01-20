import json, urllib

class Session:
    def __init__(self, api, id, id_from, id_to, active, start_time, end_time, duration, comment):
        self.api = api
        self.id = id
        self.id_from = id_from
        self.id_to = id_to
        self.active = active
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.comment = comment

    def row(self):
        return [
            self.id,
            self.id_from.id,
            self.id_from.alias,
            self.id_to.id,
            self.id_to.alias,
            self.start_time,
            self.end_time,
            self.duration,
            self.comment
        ]

    def change_comment(self, comment):
        self.api.patch("sessions/" + str(self.id), json.dumps({"comment": comment}))
        self.comment = comment

    def close(self):
        try:
            self.api.post("sessions/" + str(self.id) + "/action", json.dumps({"action": "close"}))
            self.active = False
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Session already closed")
            else:
                raise err
