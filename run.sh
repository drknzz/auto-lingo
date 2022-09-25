#!/usr/bin/bash
function displayUsage() {
    echo "
Usage: $0 <command>
<command>:
    help
        Display this help message.
    number
        Desired number of windows
    get-ready
        Makes bot ready to run
"
}

function codeRun() {
    for i in $(seq 1 $1)
    do
    gnome-terminal -- bash -c "python3 auto-lingo.py -a -n $i; exec bash"
    sleep 5
    done
}

function getReady() {
    # install pip and virtualenv
    if ! [ -x "$(command -v virtualenv)" ]; then
        echo "Pip is installing"
        sudo apt-get install python3-pip
        echo "Virtualenv is installing"
        sudo pip3 install virtualenv 
    fi

    virtualenv venv
    source venv/bin/activate

    pip install selenium
}

function main() {
    case "${1-}" in
        help)
            displayUsage
            ;;
        number)
            codeRun $2
            ;;
        get-ready)
            getReady
            ;;
        *)
            >&2 echo "Error: Unknown command: '${1-}'"
            >&2 displayUsage
            exit 1
    esac
}

main "$@"
