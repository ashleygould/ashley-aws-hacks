#!/bin/bash
set -x

cp bin/* ~/bin/
[ -d ~/.profile.d ] || mkdir ~/.profile.d
cp profile.d/* ~/.profile.d/




