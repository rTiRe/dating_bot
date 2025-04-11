#!/bin/bash

declare -A scripts=(
    ['start']='./start.sh'
    ['start_attached']='./start_attached.sh'
    ['stop']='./stop.sh'
    ['restart']='./restart.sh'
    ['rebuild']='./rebuild.sh'
    ['logs']='./logs.sh'
)

declare -A services=(
    ['accounts']='accounts_service'
)

service=""
if [ $# -ge 2 ]; then
    if [[ -v services[$2] ]]; then
        service=${services[$2]}
    else
        echo "Service \"$2\" does not exists"
        exit 1
    fi
fi

if [ $# -ge 1 ]; then
    if [[ -v scripts[$1] ]]; then
        directory=$(dirname $0)
        ${directory}/${scripts[$1]} ${service}
    else
        echo "Script \"$1\" does not exists"
        exit 1
    fi
fi