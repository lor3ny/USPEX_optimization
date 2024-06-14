# Set environment variable for USPEX path
USPEX_PATH = "/gpfs/data/fs71990/cataldo2/programs_vsc5/USPEX_v10.5/application/archive"
USPEX = USPEX_PATH + "/USPEX"  # Assuming path concatenation

# Initialize variables
break_free = 0

# Print starting message
print "Starting USPEX.."

# Loop until a file named 'USPEX_IS_DONE' is found
while (file_exists("USPEX_IS_DONE") == False):
  # Append current date to a log file
  append_to_file("log", get_current_date())

  # Run USPEX with redirection to append output to the log file
  execute_command(USPEX + " -r >> log") # MOST IMPORTANT LINE

  # Sleep for 60 seconds

  # Check for a file named 'still_running' (optional waiting)
  counter = 0
  while (file_exists("still_running") == True):
    counter = counter + 1
    sleep 10
    if (counter > 30):
      print "USPEX still running for too long, exiting.."
      break_free = 1
      break  # Exit the inner loop

  # Check break flag after inner loop
  if (break_free == 1):
    break  # Exit the outer loop

# Print finishing message
print "USPEX finished!"

