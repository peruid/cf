#!/usr/bin/env bash
cd /usr/sys/etc/farmusers
for u in *;do WHEN=$(ls -l -D "%Y-%m-%d" $u/tariff | awk '{print $6}'); grep -q -E "_(bitrix|wp|joom|402|502|602)[0-9]+$" $u/tariff && ( printf "%s:DOGOVOR:" $u; cat $u/tariff; printf ":%s:" $WHEN; cat $u/quota_disk; echo "");done
