USPEX_PATH="/gpfs/data/fs71990/cataldo2/programs_vsc5/USPEX_v10.5/application/archive"
export USPEX=${USPEX_PATH}/USPEX


break_free=0
echo "Starting USPEX.."
while [ ! -f ./USPEX_IS_DONE ]; do
   date >> log
   $USPEX -r >> log
   sleep 60
   # if still_running is present uspex should wait longer to restart
   counter=0
   while [ -f ./still_running ]; do
	 counter=$(echo "${counter}+1" | bc)
	 sleep 10
	if [ ${counter} -gt 30 ]
	then
		echo "USPEX still for too long, exiting.."
		break_free=1
		break
	fi
	done
   if [ $break_free -eq 1 ]
   then
	   break
   fi
done
echo "USPEX finished!"
