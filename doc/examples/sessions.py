# --------------
# Library import
# --------------
import sys					# Import the system library
sys.path.append("../../")	# Set the working directory two folder above
import anydesk, time


# --------------------
# Variable declaration
# --------------------
api = anydesk.API(path="auth.cfg")


# Number of sessions 10 seconds ago
sessions_10_seconds_ago = api.query_sessions(start=int(time.time()) - 10)
print(len(sessions_10_seconds_ago), "Sessions 10 seconds ago")

# Print the duration of the 5 longest sessions
print("\nLongest sessions:")
longest_sessions = api.query_sessions(sort="duration", limit=5)
for session in longest_sessions:
    print(str(session.duration) + "s")

incoming_sessions 		= api.query_sessions(direction="in", limit=10)
more_incoming_sessions 	= api.query_sessions(direction="in", limit=10, offset=10)
outgoing_sessions 		= api.query_sessions(direction="out", limit=10)
