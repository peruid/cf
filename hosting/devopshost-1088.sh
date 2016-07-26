#!/usr/bin/env bash
HOST_SELF=$(hostname)
STAT_FILE="/var/tmp/stat_{$HOST_SELF}.txt"
cd /usr/sys/etc/farmusers
for u in *;do WHEN=$(ls -l -D "%Y-%m-%d" $u/tariff | awk '{print $6}'); grep -q -E "_(((bitrix|wp|joom)[0-9]+)|(402|502|602))$" $u/tariff && ( printf "%s:DOGOVOR:" $u; cat $u/tariff; printf ":CREATE_DATE:%s:" $WHEN; cat $u/quota_disk; echo "");done > ${STAT_FILE}
