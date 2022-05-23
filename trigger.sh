#!/bin/bash

help()
{
    echo "Usage: bash trigger.sh [ -n | --number ]
                       [ -h | --help  ]"
    exit 2
}

while getopts ":n:p:" o; do
    case "${o}" in
        n)
            number=${OPTARG}
            ;;

        *)
            help
            ;;
    esac
done
shift $((OPTIND-1))

for (( i=0; i<$number; i++ ))
do
    gnome-terminal -- bash -c "python auto-lingo.py -a; exec bash"
done