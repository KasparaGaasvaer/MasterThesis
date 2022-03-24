#!/bin/bash

CURRENT_PATH="/Users/kaspara/Documents/MASTER_GIT_GAMMEL_MAC/MasterThesis/"
TARGET_PATH="/Users/kaspara/Documents/MASTER_GIT_GAMMEL_MAC/daniel_repo/plots/"
ALL_FILES=$(find ${CURRENT_PATH} -name "*plots*")

cp -r ${ALL_FILES} ${TARGET_PATH}
