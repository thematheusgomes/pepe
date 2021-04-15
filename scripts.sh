# set -e
ENVPATH=".venv"
VLOCK="0"
OLDPYTHONPATH=''

function py-env() {
    echo "py-env..."
    if [ ! -d "$ENVPATH" ]; then
        echo "creating virtualenv..."
        virtualenv -p python3 $ENVPATH
    fi
    if [ "$VLOCK" = "1"  ]; then
        echo "VLOCK is set! ignoring export PYTHONPATH and source $ENVPATH/bin/activate"
    fi
    if [ "$VLOCK" = "0" ]; then
        VLOCK="1"
        OLDPYTHONPATH=$PYTHONPATH
        echo "activate environment..."
        export PYTHONPATH=$PYTHONPATH:${PWD}/.venv/bin/python:${PWD}/src:${PWD}
        source $ENVPATH/bin/activate
    fi
}

function py-d-env() {
    if [ "$VLOCK" = "1"  ]; then
        export PYTHONPATH=$OLDPYTHONPATH
        VLOCK="0"
        deactivate
    fi
}

function py-update-pip() {
    pip install --upgrade pip
}

function py-install() {
    py-env
    py-update-pip
    echo "Installing Python Modules..."
    pip3 install -r ./requirements.txt
    echo "Installing Serverless Framework..."
    npm install
}

function py-deploy() {
    npm install
    serverless deploy --stage dev
}

function py-destroy() {
    npm install
    serverless remove --stage dev
}

function py-prod-deploy() {
    npm install
    serverless deploy --stage prod
}
