#!/bin/bash
set -e

#=================#
#   SSM           #
# PARAMETER STORE #
#=================#

if [ -n "$COMMON_SSM_PARAMETER_PATH" ]
then
    echo Exporting Parameters from $COMMON_SSM_PARAMETER_PATH
    aws --region $AWS_REGION ssm get-parameters-by-path --path $COMMON_SSM_PARAMETER_PATH --with-decryption --query Parameters | jq -r 'map("\(.Name | sub("'$COMMON_SSM_PARAMETER_PATH'";""))=\(.Value)") | join("\n")' >> /tmp/common_secrets.env
    echo "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" >> /tmp/common_secrets.env
    eval $(cat /tmp/common_secrets.env | sed 's/^/export /' | sudo tee -a /etc/profile.d/common_secrets.sh)
    eval $(cat /tmp/common_secrets.env >> /etc/environment)
    echo -n $GOOGLE_TOKEN | base64 --decode > /opt/app/token.json
    echo -n $GOOGLE_CREDS | base64 --decode > /opt/app/credentials.json
fi


#=========#
#   SSM   #
#=========#

# Register instance on SSM
if [ -n "$INSTANCE_NAME" ]; then
    echo Creating Activation Key with AWS SSM
    read -r ACTIVATION_CODE ACTIVATION_ID <<< $(aws ssm create-activation --default-instance-name "${INSTANCE_NAME}" --iam-role "ZYDSSMROLE" --registration-limit 1 --region ${AWS_DEFAULT_REGION} --tags "Key=Name,Value=${INSTANCE_NAME}" "Key=Type,Value=fargate" --query "join(' ', [ActivationCode, ActivationId])" --output text)
    echo Registering SSM Code
    sudo amazon-ssm-agent -register -code "${ACTIVATION_CODE}" -id "${ACTIVATION_ID}" -region "${AWS_DEFAULT_REGION}" -clear -y
    echo Starting SSM Agent Services
    sudo amazon-ssm-agent 2>&1 &
    export INSTANCE_ID=$(sudo cat /var/lib/amazon/ssm/registration | jq -r .ManagedInstanceID)
    echo $INSTANCE_ID
fi

#=========#
#   CWA   #
#=========#
## Please change the region accordingly to match your AWS Region
if [ -n "$CWA_CONFIG" ]
then
    echo Downloading CWA config
    echo $CWA_CONFIG | sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json    # CONFIG CWA
    echo -e '[credentials]\nshared_credential_profile = "default"\nshared_credential_file = "/root/.aws/credentials"' | sudo tee -a /opt/aws/amazon-cloudwatch-agent/etc/common-config.toml
    sudo /opt/aws/amazon-cloudwatch-agent/bin/start-amazon-cloudwatch-agent &
fi

# Unregister instance from SSM on SIGTERM
term_handler() {
    if [ -n "$INSTANCE_NAME" ]; then
        aws ssm deregister-managed-instance --region ${AWS_DEFAULT_REGION} --instance-id $(sudo cat /var/lib/amazon/ssm/registration | jq -r .ManagedInstanceID)
        echo "SSM instance Unregistered"
        exit 143; # 128 + 15 -- SIGTERM
    fi
}
trap 'term_handler' SIGTERM SIGINT ERR

exec "$@"