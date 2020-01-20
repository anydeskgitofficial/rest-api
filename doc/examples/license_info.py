# --------------
# Library import
# --------------
import sys					# Import the system library
import time
sys.path.append("../../")	# Set the working directory two folder above
import anydesk


# --------------------
# Variable declaration
# --------------------
api = anydesk.API(path="auth.cfg")
license = api.sysinfo().license


print("Name:", license.name)
print("Expires:", time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(license.expires)))
print("Max Clients:", license.max_clients if license.max_clients > 0 else "unlimited")
print("Max Sessions:", license.max_sessions if license.max_sessions > 0 else "unlimited")
print("Max Session Time:", license.max_session_time if license.max_session_time > 0 else "unlimited")
print("License Id:", license.license_id)
print("License Key:", license.license_key)
print("API Key:", license.api_password)

print("Namespaces:")
for namespace in license.namespaces:
    print(" @"+namespace.name, "(" + str(namespace.size) + " entries)")
