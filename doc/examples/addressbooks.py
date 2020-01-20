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


for addressbook in api.all_addressbooks():
    print(addressbook.name, "(" + str(addressbook.id) + ")")
