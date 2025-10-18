#!/bin/bash

echo "Refreshing all cards sets in card_set_lookup"
for FILE in card_set_lookup/*.json; do
	SET_ID=$(basename "$FILE" .json)
	echo "Updating card data for: $SET_ID"
	curl -s "https://api.pokemontcg.io/v2/sets/$SET_ID" -o $FILE
	echo "Updated data in $FILE"
done
echo "All card sets have been refreshed." 
