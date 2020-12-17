# set -e
ENVPATH=".venv"
VLOCK="0"
PROJECT="pepe"
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

function py-update-pip() {
    pip install --upgrade pip
}

function py-install() {
    py-env
    py-update-pip
    echo "[production] py-install..."
    pip3 install -r ./requirements.txt
}

function py-install-dev() {
    py-env
    py-update-pip
    echo "[development] py-install..."
    pip3 install -r ./requirements.dev.txt
    npm install
}

function lambda-permissions() {
    cd $1
    chmod 755 $(find $(pwd) -type d)
    chmod 644 $(find $(pwd) -type f)
    cd ..
}

function py-zip() {
    py-d-env
    py-env
    cp -R ./waf.json ./build
    cp -R ./src/lambda.py ./build/
    cp -R ./src/main ./build
    lambda-permissions ./build
    cd ./build
    zip -q -rMM9 $PROJECT.zip .
    mv $PROJECT.zip ../
    cd ..
    py-d-env
}

function py-build() {
    py-d-env
    py-env
    rm -rf $ENVPATH/ ./build/ $(find ./src/ -name __pycache__) $PROJECT.zip
    mkdir ./build
    py-install
    py-zip
    py-d-env
    rm -rf $ENVPATH/ $(find ./src/ -name __pycache__)
    py-install-dev
}
