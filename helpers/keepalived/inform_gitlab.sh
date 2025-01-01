#!/bin/sh

# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# WARNING: Do not use this script in pipelines! Tokens will be added as command line arguments

CURL_BIN=$(which curl)

if [ -n "$CURL_BIN" ];
then
  echo "ERROR: No curl detected!"
  exit 2
fi

# Gitlab URL including the repository location/api
GITLAB_URI=$1
if [ -n "$GITLAB_URI" ];
then
  echo "ERROR: URL (including repository) is necessary."
  exit 2
fi

# Define the GITLAB access token. It needs permissions to start pipelines
if [ -n "$GITLAB_TOKEN" ];
then
  if [ -n "$2" ];
  then
    echo "ERROR: You need to specify an api token."
  else
    GITLAB_TOKEN=$2
  fi
fi

# Define the git reference (commit hash, branch or tag name)
if [ -n "$GITLAB_REF" ];
then
  if [ -n "$2" ];
  then
    GITLAB_REF="main"
  else
    GITLAB_REF="$2"
  fi
fi

# Define optional variables. If you want to pass job variables,
# you have to define them as follows:
# variables[VARIABLE_NAME]=VALUE
if [ -n "$GITLAB_VARIABLES" ];
then
  GITLAB_VARIABLES="$3"
else
  GITLAB_VARIABLES="-F $GITLAB_VARIABLES"
fi

# Do the curl
$CURL_BIN -L --silent \
  -X POST \
  -F token="$GITLAB_TOKEN" \
  -F "ref=$GITLAB_REF" \
  "$GITLAB_VARIABLES" \
  "$GITLAB_URI"
