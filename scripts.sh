# set -e
ENVPATH=".venv"
VLOCK="0"
PROJECT="pepe"
OLDPYTHONPATH=''

function py-env() {
    echo "py-env..."
    if [ ! -d "$ENVPATH" ]; then
        echo "creating virtualenv..."
        virtualenv -p python3.6 $ENVPATH
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

function aws-check() {
    if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_SESSION_TOKEN" ]
    then
      echo " [WARN] Missing AWS permission using env: "
      echo "- \$AWS_ACCESS_KEY_ID"
      echo "- \$AWS_SECRET_ACCESS_KEY"
      echo "- \$AWS_SESSION_TOKEN"
      echo "$YELLOW [WARN] The following commands will fail if no credentials are configured on fallback ~/.aws/config $YELLOW"

    fi
}

function py-install() {
    py-env
    echo "[production] py-install..."
    pip install -r dependecies/requirements.txt
    npm install
}

