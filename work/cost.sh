#!/bin/bash

# -w オプションでwatch機能を有効にする
if [ "$1" = "-w" ]; then
    watch -n 1 --color "npx ccusage@latest"
else
    npx ccusage@latest
fi