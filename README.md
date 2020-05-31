# apcupsmon, A light weight plot and logging tool for APC Backup UPS BR1000G
A program to plot and log APC UPS via apcupsd daemon.

**Install**  
  &nbsp;&nbsp;&nbsp;&nbsp;```cd /tmp```  
  &nbsp;&nbsp;&nbsp;&nbsp;```git clone https://github.com/abhiramshibu/apcupsmon```  
  &nbsp;&nbsp;&nbsp;&nbsp;```cd apcupsmon```  
  &nbsp;&nbsp;&nbsp;&nbsp;```sudo make install```  
  &nbsp;&nbsp;&nbsp;&nbsp;```cd ../```  
  &nbsp;&nbsp;&nbsp;&nbsp;```rm -rf apcupsmon```  
  <br>
**Usage**  
  &nbsp;&nbsp;&nbsp;&nbsp;```apcupsmon -h``` to display help  
  &nbsp;&nbsp;&nbsp;&nbsp;```apcupsmon -l -p``` to plot  
  &nbsp;&nbsp;&nbsp;&nbsp;```apcupsmon -p``` to log to /var/log/apcupsmon and plot  
  &nbsp;&nbsp;&nbsp;&nbsp;```apcupsmon -a <file>``` to analyze the energy usage in that log file   
  &nbsp;&nbsp;&nbsp;&nbsp;For advanced help, use -h or --help to see other arguments.
