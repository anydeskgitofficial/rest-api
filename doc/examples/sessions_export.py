# ================
# Library import
# ================
import sys                    # Import the system library
sys.path.append("../../")     # Set the working directory two folder above
import anydesk
import time
import csv
from datetime import datetime, timedelta
from time import mktime

def main(argv):    
    # ================
    # The following is direct input by calling the functions, the customer wants, directly (via a script for example)
    # ================
    if (len(argv) > 0):
        if (argv[0] == "inbetween_dates"):
            if (len(argv) < 4):
                print("To less arguments entered, exiting...")
                sys.exit()
            elif (len(argv) > 5):
                print("To much arguments entered, exiting...")
                sys.exit()
            
            if (len(argv) == 4):
                filter_session_inbetween_dates(argv[1], argv[2], argv[3])
            elif (len(argv) == 5):
                filter_session_inbetween_dates(argv[1], argv[2], argv[3], argv[4])
            
            sys.exit()
        elif (argv[0] == "duration_and_count"):
            if (len(argv) < 3):
                print("To less arguments entered, exiting...")
                sys.exit()
            elif (len(argv) > 4):
                print("To much arguments entered, exiting...")
                sys.exit()
            
            if (len(argv) == 3):
                filter_session_by_duration_and_count(argv[1], argv[2])
            elif (len(argv) == 4):
                filter_session_by_duration_and_count(argv[1], argv[2], argv[3])
            
            sys.exit()
        elif (argv[0] == "Help" or argv[0] == "help"):
            display_help()
            sys.exit()
        else:
            print("Not a valid command, please use \"Help\" or \"help\" as parameter to display the help.")
            sys.exit()
    
    # ================
    # Everything below is handeled by console input
    # ================
    input_result = ""
    
    while (input_result != "4" and input_result != "4."):
        print("\n========================================\nChoose one of the following options:\n========================================\n")
        print(" 1. Display sessions between two dates")
        print(" 2. Display sessions by duration and count (sorting down from the longest)")
        print(" 3. Help")
        print(" 4. Exit\n")
        
        input_result = input()
        
        if (input_result == "1" or input_result == "1."):
            # Get start date by the console input
            print("Enter the start date - e.g. the format MUST be either \"01.01.2019\" or \"01.01.2019 11:11:11\":")
            start_date_input = input()
            # Get end date by the console input
            print("Enter the end date - e.g. the format MUST be either \"02.01.2019\" or \"02.01.2019 11:11:11\":")
            end_date_input = input()
            # Get the csv export by the console input
            print("Enter \"true\" if you want to export the data to a csv file, otherwise enter \"false\" or leave empty:")
            export_input = input()
            filename_input = ""
            if (export_input == "true"):
                # The user can specify a filename here or leave it empty for the standard filename
                print("If you want to specify a filename, just enter it, leave it empty and press return/enter:")
                filename_input = input()
            
            filter_session_inbetween_dates(start_date_input, end_date_input, export_input, filename_input)
        elif (input_result == "2" or input_result == "2."):
            
            # Get the count by the console input
            print("Enter, how many sessions you want to filter:")
            count_input = input()
            # Get the csv export by the console input
            print("Enter \"true\" if you want to export the data to a csv file, otherwise enter \"false\" or leave empty:")
            export_input = input()
            # The user can specify a filename here or leave it empty for the standard filename
            print("If you want to specify a filename, just enter it, leave it empty and press return/enter:")
            filename_input = input()
            
            filter_session_by_duration_and_count(count_input, export_input, filename_input)
        elif (input_result == "3" or input_result == "3."):
            # Call the helper function
            display_help()
        elif (input_result == "4" or input_result == "4."):
            print("Exiting the script...")
            sys.exit()
        else:
            print("No vaild selection, please select one of the option above")

def display_help():
    print("\n============================\nHelp for the script file:\n============================\n")
    print(" - You can use the functions directly or simply navigate through the menu to export/display the filtered data.\n")
    print(" - Function explanation:")
    print("     inbetween_dates:    Filter sessions between two specified dates; if no time is used, it will use 00:00:00 (i.e. \"01.01.2019 00:00:00\") for the start date and 23:59:59 (i.e. \"02.01.2019 23:59:59\") for the end date.")
    print("     duration_and_count: Filter sessions by a specified count, downwards from the longest session (it is always sorted by duration).\n")
    print(" - In both functions, if the parameter for file-export is set to false, the data will be displayed directly in the console (also no parameter for the filename is needed).\n")
    print(" - Either use \"inbetween_dates\" or \"duration_and_count\" to directly call the function without navigating through the menu (i.e. to use it in a script file).")
    print("   The parameters for the functions are as follows:\n")
    print("   inbetween_dates    start-date (\"01.01.2019\" or \"01.01.2019 11:11:11\")")
    print("                      end-date (\"02.01.2019\" or \"02.01.2019 11:11:11\"")
    print("                      file-export (true or false)")
    print("                      filename (leave empty or a specific name)")
    print("   Final use example: python.exe sessions_export.py inbetween_dates \"01.01.2019\" \"02.01.2019\" \"true\" \"test_export_file\"\n")
    print("   duration_and_count session-count filter (sorted from the longest downwards)")
    print("                      file-export (true or false)")
    print("                      filename (leave empty or a specific name)")
    print("   Final use example: python.exe sessions_export.py duration_and_count \"10\" \"true\" \"test_export_file\"\n")
    print("Press any key to continue...")
    input()

def filter_session_inbetween_dates(date_one, date_two, export_to_csv, filename=""):
    # ====================
    # Variable declaration
    # ====================
    api          = anydesk.API(path="auth.cfg")
    sessions     = []
    buffer_start = date_one
    buffer_end   = date_two
    
    if (len(buffer_start) == 10):
        buffer_start += " 00:00:00"
    
    if (len(buffer_end) == 10):
        buffer_end += " 23:59:59"
    
    if (filename == ""):
        filename = "../../sessions_inbetween_dates_" + str(datetime.now().strftime("%d.%m.%Y_%H-%M-%S")) + ".csv"
    else:
        filename = "../../" + filename + ".csv"
    
    # Format:                                          (year, month, day, hour, minute, second)
    filter_start_time = datetime.strptime(buffer_start, '%d.%m.%Y %H:%M:%S')
    filter_end_time   = datetime.strptime(buffer_end, '%d.%m.%Y %H:%M:%S')
    
    longest_sessions = api.query_sessions(sort="duration")
    
    for session in longest_sessions:
        
        session_start_time = datetime.fromtimestamp(time.mktime(time.gmtime(session.start_time)))
        session_end_time   = datetime.fromtimestamp(time.mktime(time.gmtime(session.end_time)))
        
        if (session_start_time >= filter_start_time and session_end_time <= filter_end_time):
            
            # Calculate the duration in seconds, minutes, hours and days
            session_id         = session.id
            from_ID            = session.id_from.id
            from_alias         = session.id_from.alias
            to_ID              = session.id_to.id
            to_alias           = session.id_to.alias
            start_time_session = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(session.start_time))
            end_time_session   = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(session.end_time))
            minutes, seconds   = divmod(session.duration, 60)
            hours, minutes     = divmod(minutes, 60)
            days, hours        = divmod(hours, 24)
            comment            = session.comment
            
            if (export_to_csv == "false" or export_to_csv == ""):
                print("\n================\nSession data\n================")
                print("Session ID                = " + str(session_id))
                print("From ID                   = " + str(from_ID))
                print("From Alias                = " + str(from_alias))
                print("To ID                     = " + str(to_ID))
                print("To Alias                  = " + str(to_alias))                
                print("Start time                = " + str(start_time_session))    
                print("End time                  = " + str(end_time_session))
                print("Days                      = " + str(days))
                print("Hours                     = " + str(hours))
                print("Minutes                   = " + str(minutes))
                print("Seconds                   = " + str(seconds))
                print("Total duration in Seconds = " + str(session.duration))
                print("Comment                   = " + str(comment))
                print("================================\n")
            
            sessions.append([str(session_id),
                             str(from_ID),
                             str(from_alias),
                             str(to_ID),
                             str(to_alias),
                             str(start_time_session),
                             str(end_time_session),
                             str(days),
                             str(hours),
                             str(minutes),
                             str(seconds),
                             str(session.duration),
                             str(comment)])
    
    if export_to_csv == "true":
        
        fieldnames = ['Session ID',
                      'From ID',
                      'From Alias',
                      'To ID',
                      'To Alias',
                      'Start time',
                      'End time',
                      'Days',
                      'Hours',
                      'Minutes',
                      'Seconds',
                      'Total duration in Seconds',
                      'Comment']
        
        with open(filename, "w", newline="") as f:
            
            csv_writer = csv.writer(f)
            csv_writer.writerow(fieldnames)
            
            for i in range(len(sessions)):
                csv_writer.writerow(sessions[i])
    
    if (export_to_csv == "true"):
        print(" \n**** Data has been successfully exported to the file \"" + str(filename[6:len(filename)]) + "\" ****")
                
def filter_session_by_duration_and_count(session_limit, export_to_csv, filename=""):
    # ====================
    # Variable declaration
    # ====================
    api      = anydesk.API(path="auth.cfg")
    sessions = []
    
    if (filename == ""):
        filename = "../../sessions_duration_and_count_" + str(datetime.now().strftime("%d.%m.%Y_%H-%M-%S")) + ".csv"
    else:
        filename = "../../" + filename + ".csv"
    
    longest_sessions = api.query_sessions(sort="duration", limit=int(session_limit))
    
    for session in longest_sessions:
            
            # Calculate the duration in seconds, minutes, hours and days
            session_id          = session.id
            from_ID             = session.id_from.id
            from_alias          = session.id_from.alias
            to_ID               = session.id_to.id
            to_alias            = session.id_to.alias
            start_time_session  = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(session.start_time))
            end_time_session    = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(session.end_time))
            minutes, seconds    = divmod(session.duration, 60)
            hours, minutes      = divmod(minutes, 60)
            days, hours         = divmod(hours, 24)
            comment             = session.comment
            
            if (export_to_csv == "false" or export_to_csv == ""):
                print("\n================\nSession data\n================")
                print("Session ID                = " + str(session_id))
                print("From ID                   = " + str(from_ID))
                print("From Alias                = " + str(from_alias))
                print("To ID                     = " + str(to_ID))
                print("To Alias                  = " + str(to_alias))                
                print("Start time                = " + str(start_time_session))    
                print("End time                  = " + str(end_time_session))
                print("Days                      = " + str(days))
                print("Hours                     = " + str(hours))
                print("Minutes                   = " + str(minutes))
                print("Seconds                   = " + str(seconds))
                print("Total duration in Seconds = " + str(session.duration))
                print("Comment                   = " + str(comment))
                print("================================\n")
            
            sessions.append([str(session_id),
                             str(from_ID),
                             str(from_alias),
                             str(to_ID),
                             str(to_alias),
                             str(start_time_session),
                             str(end_time_session),
                             str(days),
                             str(hours),
                             str(minutes),
                             str(seconds),
                             str(session.duration),
                             str(comment)])
    
    if (export_to_csv == "true"):
        
        fieldnames = ['Session ID',
                      'From ID',
                      'From Alias',
                      'To ID',
                      'To Alias',
                      'Start time',
                      'End time',
                      'Days',
                      'Hours',
                      'Minutes',
                      'Seconds',
                      'Total duration in Seconds',
                      'Comment']
        
        with open(filename, "w", newline="") as f:
            
            csv_writer = csv.writer(f)
            csv_writer.writerow(fieldnames)
            
            for i in range(len(sessions)):
                csv_writer.writerow(sessions[i])
    
    if (export_to_csv == "true"):
        print(" \n**** Data has been successfully exported to the file \"" + str(filename[6:len(filename)]) + "\" ****")
    
if __name__ == "__main__":
   main(sys.argv[1:])