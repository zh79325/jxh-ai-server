#!/bin/bash
ACTION=$1
APP_START_TIMEOUT=120    # 等待应用启动的时间
SERVER_PORT=8010
HEALTH_CHECK_URL=http://127.0.0.1:${SERVER_PORT}/info
IMAGE_NAME=jxh_ai
CONTAINER_NAME=jxh_ai_container
# Convenience function for logging text to stdout in pretty colors.
function log {
    local message="$@"

    local green="\\033[1;32m"
    local reset="\\033[0m"

    if [[ $TERM == "dumb" ]]
    then
        echo "${message}"
    else
        echo -e "${green}${message}${reset}"
    fi
}

# Check if a container with a given name already exists
function container_exists {
    local container_name=$1

    if [[ -z "$(docker ps -a | grep ${container_name})" ]]
    then false
    else true
    fi
}

function container_running {
    local container_name=$1

    if [[ -z "$(docker container ls  | grep ${container_name})" ]]
    then false
    else true
    fi
}

# Get the image tag version based on the git SHA
function version {
    cat server.version
}

health_check() {
    exptime=0
    echo "checking ${HEALTH_CHECK_URL}"
    while true
        do
            status_code=`/usr/bin/curl -L -o /dev/null --connect-timeout 5 -s -w %{http_code}  ${HEALTH_CHECK_URL}`
            if [ "$?" != "0" ]; then
               echo -n -e "\rapplication not started"
            else
                echo "code is $status_code"
                if [ "$status_code" == "200" ];then
                    break
                fi
            fi
            sleep 1
            ((exptime++))

            echo -e "\rWait app to pass health check: $exptime..."

            if [ $exptime -gt ${APP_START_TIMEOUT} ]; then
                echo 'app start failed'
               exit 1
            fi
        done
    echo "check ${HEALTH_CHECK_URL} success"
}

status() {
    if container_running ${container_name}
        then
            log "container ${container_name} is running"
        else
            log "container ${container_name} not running"
    fi

    if container_exists ${container_name}
        then
            log "container ${container_name} exists"
        else
            log "container ${container_name} not exist"
    fi
}

# Build the Docker image and deploy it to a given Docker machine and
# give the container a specific name.
# Remove any containers that already exist with the given name.
function deploy {
    local image_name=$1
    local container_name=$2

    log "pull base run time image"
    docker pull registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:runtime

    log "Building image"
    docker build --tag ${image_name}:$(version) .

    status

    if container_running ${container_name}
    then
        log "stop exiting container"
        docker container stop ${container_name}
    fi

    if container_exists ${container_name}
    then
        log "Deleting exiting container"
        docker rm -f ${container_name}
    fi

    log "Starting containter"
    docker run \
        --restart=unless-stopped \
        --detach \
        --publish ${SERVER_PORT}:${SERVER_PORT} \
        --name ${container_name} \
        ${image_name}:$(version)
    health_check
    log "Now running on http://127.0.0.1:${SERVER_PORT}"
}

#
# Main
#

start() {
    deploy  ${IMAGE_NAME} ${CONTAINER_NAME}
}



case "$ACTION" in
    start)
        start
    ;;
    status)
        status
    ;;
esac
#docker pull registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
#docker run -d -p 8010:8010 registry.cn-hangzhou.aliyuncs.com/ali-build/jxh-ai-server:latest
