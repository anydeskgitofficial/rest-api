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
session = api.query_sessions(limit=1)[0]


print("Id:", session.id)
print("Id from:", session.id_from.id)
print("Alias from:", session.id_from.alias)
print("Id to:", session.id_to.id)
print("Alias to:", session.id_to.alias)
print("Active:", session.active)
print("Start time:", session.start_time)
print("End time:", session.end_time)
print("Duration:", session.duration)
print("Comment:", session.comment)

print()

def print_client(client):
    print("Id:", client.id)
    print("Alias:", client.alias)
    print("Version:", client.version)
    print("Online:", client.is_online)
    print("Online Time:", client.online_time)
    print("Comment:", client.comment)

print("=== Client From ===")
print_client(session.id_from.client())

print()
print("==== Client To ====")
print_client(session.id_to.client())
