#!/usr/bin/env bash

read -p  "TCG Card Set ID: " SET_ID
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi
echo "Fetching data for $SET_ID"
curl --ssl-no-revoke -s "https://api.pokemontcg.io/v2/sets/$SET_ID" -o "card_set_lookup/${SET_ID}.json"
echo "Data saved to card_set_lookup/${SET_ID}.json"