
TOTAL=$(du -sc /home/* | grep total | awk '{print $1}')
# 700G = 700000000
ALERT=8500000000
if [ $TOTAL -ge $ALERT ]; then
       { du -hsc /home/* | sort -hr; echo $(date); } | tr "\n" "\n" | mail -s "[Tokyo] DISK USAGE ALERT" st121413@ait.asia
fi
