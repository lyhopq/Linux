#!/bin/bash

sudo apt-get install meld
mkdir ~/.meld
ln -s /usr/bin/meld ~/.gnome2/nautilus-scripts/比较...
cp script-worker ~/.meld/
cp scripts/* ~/.gnome2/nautilus-scripts/
