#!/bin/bash

SERVICE_NAME="fancontrol"
SERVICE_FILE="$SERVICE_NAME.service"
DESCRIPTION="Raspberry Fan Control"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
touch SERVICE_FILE
cat > $DIR/SERVICE_FILE <<EOL
[Unit]
Description=${DESCRIPTION}

[Service]
Restart=always
User=${USER}
WorkingDirectory=${DIR}
ExecStart=pipenv run python main.py >> ${DIR}/log.txt 2>&1

[Install]
WantedBy=multi-user.target
EOL

sudo cp $SERVICE_FILE /lib/systemd/system/
sudo systemctl daemon-reload
echo "USE: 'sudo service $SERVICE_NAME' to Start"

