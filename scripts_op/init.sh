#!/bin/bash

cd LittleBeeGeo_backend
virtualenv __
. __/bin/activate
pip install -r requirements.txt
cd ..
deactivate

cd LittleBeeGeo_crawlers
virtualenv __
. __/bin/activate
pip install -r requirements.txt
cd ..
deactivate

cd LittleBeeGeo-frontend
./scripts/init.sh
cd ..
