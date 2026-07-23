#!/bin/sh
LIMIT=85
while true; do
 t=0
 for h in /sys/class/hwmon/hwmon*; do [ "$(cat $h/name 2>/dev/null)" = k10temp ] && t=$(awk '{printf "%d",$1/1000}' "$h/temp1_input"); done
 cur=$(awk -F= '/frequency/{print $2}' /etc/bc250-smu-oc.conf|tr -d ' '|head -1)
 if [ "$t" -gt "$LIMIT" ] && [ -n "$cur" ] && [ "$cur" -gt 3500 ]; then new=$((cur-100)); sed -i "s/^frequency = .*/frequency = $new/" /etc/bc250-smu-oc.conf; systemctl stop cyan-skillfish-governor 2>/dev/null; python3 /opt/bc250_smu_oc/bc250_apply.py --apply /etc/bc250-smu-oc.conf 2>/dev/null; systemctl start cyan-skillfish-governor 2>/dev/null; fi
 sleep 10
done
