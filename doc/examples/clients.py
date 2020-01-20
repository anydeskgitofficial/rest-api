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


def print_clients(clients):
    for client in clients:
        if client.alias == None:
            print(str(client.id))
        else:
            print(str(client.id), "("+client.alias+")")
    print()

print("Online:")
online_clients = api.query_clients(online=True)
print_clients(online_clients)

print("Not in own namespace:")
ad_clients = api.query_clients(filter="@ad")
print_clients(ad_clients)

print("Sorted by alias:")
clients_sorted_by_online = api.query_clients(sort="alias")
print_clients(clients_sorted_by_online)
