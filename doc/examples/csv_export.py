# --------------
# Library import
# --------------
import sys					# Import the system library
sys.path.append("../../")	# Set the working directory two folder above
import anydesk


# --------------------
# Variable declaration
# --------------------
api = anydesk.API(path="auth.cfg")


with open("sessions.csv", "w", newline="") as f:
	csv = anydesk.SessionCSV(f)
	csv.write(api.all_sessions())

with open("online_clients.csv", "w", newline="") as f:
    csv = anydesk.ClientCSV(f)
    csv.write(api.query_clients(online=True))
