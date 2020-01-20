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
sysinfo = api.sysinfo()


# System information
print("Name:            ", sysinfo.name)
print("Version:         ", sysinfo.version)
print("Client Count:    ", sysinfo.client_count)
print("Online Clients:  ", sysinfo.online_count)
print("Session Count:   ", sysinfo.session_count)
print("Active Sessions: ", sysinfo.active_session_count)