from csv import writer

class CSV:
    def __init__(self, f, dialect="excel"):
        f.write("sep=,\n")
        self.writer = writer(f, dialect=dialect)

    def write_row(self, obj):
        self.writer.writerow(obj.row())

    def write(self, objs):
        for obj in objs:
            self.write_row(obj)
        return self

class SessionCSV(CSV):
    def __init__(self, f):
        super(SessionCSV, self).__init__(f)
        self.writer.writerow([
            "Session Id",
            "From Id",
            "From Alias",
            "To Id",
            "To Alias",
            "Start",
            "End",
            "Duration",
            "Comment"
        ])

class ClientCSV(CSV):
    def __init__(self, f):
        super(ClientCSV, self).__init__(f)
        self.writer.writerow([
            "Client Id",
            "Alias",
            "Online Time",
            "Version",
            "Comment"
        ])

class Session_TestCSV(CSV):
    def __init__(self, f):
        super(Session_TestCSV, self).__init__(f)
        self.writer.writerow([
            "Start time",
            "End time",
            "Detailed duration",
            "total duration"
        ])