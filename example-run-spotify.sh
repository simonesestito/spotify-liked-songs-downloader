#!/bin/bash --
set -e

######################################################
#                                                    #
# Example script to run the Spotify download program #
# Change the SECRETS in this file, to make it work.  #
#                                                    #
######################################################


# TODO: add your Spotify client ID
export SPOTIPY_CLIENT_ID=iiiiiiiiiiiiiiiii

# TODO: add your Spotify client secret
export SPOTIPY_CLIENT_SECRET=sssssssssssssss

# TODO: change the arguments according to your preferences, if you wish
poetry run \
  python main.py \
    --refresh-liked-songs \
    --sort-liked-songs \
    --embed-lyrics
