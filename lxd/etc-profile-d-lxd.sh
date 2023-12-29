#!/bin/sh
export LXD_HOME=/opt/lxd
export PATH=${LXD_HOME}/bin:${PATH}
export MANPATH=${LXD_HOME}/man:${MANPATH}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LXD_HOME/lib64
