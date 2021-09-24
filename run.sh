if [ -n "$SECRETS_ID" ]
then
    echo Exporting secrets
    aws secretsmanager get-secret-value --secret-id ${SECRETS_ID} --query SecretString \
    --output text | jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' > /opt/secrets.env
    USER_SSH_KEYS_FOLDER=~/.ssh
    mkdir -p $USER_SSH_KEYS_FOLDER
    eval $(cat /opt/secrets.env | sed 's/^/export /')

    echo Exporting comlepleted

    echo Starting Scrapyd
    exec scrapyd --pidfile=/var/twisted.pid
fi
