#!/usr/bin/env bash

BACKUP_DIR=/var/backup
APP_NAME=typo
DB_NAME=typo
DB_USER=typo
DAYS_TO_KEEP_LOCAL_BACKUPS=7
DATE=$(eval date +%Y%m%d)
LOG_DIR=/var/log/${APP_NAME}
LOG=${LOG_DIR}/${DB_NAME}_backup.log

# variables passed from outside:
#
# HOOK_URL - for notifications
# STORAGE_USER, STORAGE_KEY - Selectel storage credentials
# STORAGE_DIR - Selectel storage directory

# redirect output to log file

if [ ! -d "$BACKUP_DIR" ]
then
    echo "Backup directory \"${BACKUP_DIR}\" doesn't exist"
    exit 1
fi

if [ ! -d "$LOG_DIR" ]
then
    echo "Log directory \"${LOG_DIR}\" doesn't exist"
    exit 1
fi

exec >${LOG} 2>&1

if [ -z "$1" ]
then
    echo "Config file not specified"
    exit 1
fi

source $1

function check_param() {
    local name=$1
    local param=${!name}
    if [ -z "${param}" ]; then
        echo "${name} is not set"
        exit 1
    fi
}

check_param "HOOK_URL"
check_param "STORAGE_USER"
check_param "STORAGE_KEY"
check_param "STORAGE_DIR"

CURRENT_BACKUP_FILENAME=${BACKUP_DIR}/${DB_NAME}-${DATE}.tar.gz

function send_report() {
    local code=$1
    local reason=$2
    if [ ${code} -eq 0 ]; then
        MESSAGE="${DATE} backup successfully completed"
    else
        MESSAGE="${DATE} backup failed with reason: ${reason}"
    fi
    PAYLOAD="payload={\"channel\": \"#system\", \"username\": \"backup-bot\", \"text\": \"${MESSAGE}\"}"
    curl -X POST --data-urlencode "${PAYLOAD}" ${HOOK_URL}
    exit ${code}
}

# dump typo db
pg_dump -U ${DB_USER} -Ft ${DB_NAME} | gzip -c > ${CURRENT_BACKUP_FILENAME}
if [ $? -ne 0 ]; then send_report 1 "dump failed"; fi

# send backup to selectel storage
supload -u ${STORAGE_USER} -k ${STORAGE_KEY} -d 7d ${STORAGE_DIR} ${CURRENT_BACKUP_FILENAME}
if [ $? -ne 0 ]; then send_report 1 "supload failed"; fi

# rm files older than X days
find ${BACKUP_DIR}* -mtime +${DAYS_TO_KEEP_LOCAL_BACKUPS} -exec rm {} \;
if [ $? -ne 0 ]; then send_report 1 "delete old backups failed"; fi

send_report 0
