#!/bin/sh

BINARY_PATH=/usr/bin/
BINARY_NAME=gw
DIST_DIR=/opt/gateway-autoinstall
MONGO_PASSW=$(openssl rand -base64 24 | sed -e 's/\///g')
MQTT_PASSW=$(openssl rand -base64 24 | sed -e 's/\///g')
# sudo apt install -y docker.io


downloadSources() {
    mkdir -p $DIST_DIR
    cd $DIST_DIR
    # curl -fsSL https://get.Docker.com -o get-Docker.sh
    # bash get-Docker.sh
    wget https://bchwtz.github.io/bchwtz-gateway/dist/gw-arm
    wget https://bchwtz.github.io/bchwtz-gateway/dist/docker-compose.yml
    wget https://bchwtz.github.io/bchwtz-gateway/dist/docker-compose.rpi.yml
    wget https://bchwtz.github.io/bchwtz-gateway/dist/.env-default
    wget https://bchwtz.github.io/bchwtz-gateway/dist/uninstall-gw.sh
    mv docker-compose.yml docker-compose.std.yml
    IS_32=$(uname -a | grep -i armv7l)
    if [ ! -z "$IS_32" ] ; then
        echo "Patching mongo image to comply to 32bits - consider using a 64bit-os!"
        sed -i 's/image: mongo$/image: apcheamitru\/arm32v7-mongo/' docker-compose.std.yml
        sed -i 's/\/lib\/libdbus-1\.so/\/lib\/arm-linux-gnueabihf\/libdbus-1.so.3/g' docker-compose.rpi.yml
        sed -i 's/\/lib\/libreadline\.so/\/lib\/arm-linux-gnueabihf\/libreadline.so.7/g' docker-compose.rpi.yml
    fi
    chmod +x uninstall-gw.sh
}

setupEnv() {
    if [ -f .env-default ]
    then
        echo "Configuring auto-load of env-variables"
        sed -i -e 's/\(MQTT_PASSWORD=\).*/\1"'$MQTT_PASSW'"/g' .env-default
        sed -i -e 's/\(MONGO_PASSWORD=\).*/\1"'$MONGO_PASSW'"/g' .env-default
        cp .env-default .env-local
        sed -i -e 's/\(MQTT_BROKER=\).*/\1"localhost"/g' .env-local
        awk '!/^$/{print "export " $0}' .env-local > gateway-vars.sh
        echo "INSTALLDIR=$(pwd)" >> gateway-vars.sh
        cat .env-local | sed -e 's/\(.*\)=.*$/unset \1/g' > unset-gateway-vars.sh
        echo "unset INSTALLDIR" >> unset-gateway-vars.sh

        sudo cp gateway-vars.sh /etc/profile.d/
        sudo mv $(pwd)/gw-arm $BINARY_PATH$BINARY_NAME
        sudo chmod +x $BINARY_PATH$BINARY_NAME
        chmod +x unset-gateway-vars.sh
    else
        echo "error - could not find required .env-default - please check if it is on your filesystem!"
        exit
    fi
}

run() {
    echo "Generating docker-compose"
docker compose --env-file .env-default --project-name gateway -f docker-compose.std.yml -f docker-compose.rpi.yml config > docker-compose.yml
bash $(pwd)/gateway-vars.sh
rm docker-compose.std.yml docker-compose.rpi.yml
docker compose pull
docker compose up -d
echo "Congratulations - your gateway is up and running! Please logout and login again, to load the required environment variables!"
}

update() {
    echo "Gateway already detected. Do you wish to update all components?"
    echo "Do you want to proceed? (yes/no) "

    while :
    do
        read yn
        case $yn in 
            yes ) echo ok, update started;;
            no ) echo exiting...
                exit;;
            * ) echo invalid response
                exit 1;;
        esac
        if [ $REPLY == "y" ] || [ $REPLY == "Y"]; then
            downloadSources
            run
        else
            exit
        fi
    done
}

if [ ! -f $BINARY_PATH$BINARY_NAME ] && [ ! -d $DIST_DIR ]; then
    downloadSources
    setupEnv
    run
else
    update
fi

