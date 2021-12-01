#!/bin/bash

cd /home/semenov/sanicrutor/app/

source '/home/semenov/sanicrutor/venv/bin/activate'

scrapy crawl rutor 
wait

password='14bb331a2e746694108dc37064e958a0c209da8569dfa9b3dd36c5f36ce65af8'
PGPASSWORD=$(echo $password) psql -h ec2-3-217-91-165.compute-1.amazonaws.com -U bjbvafbeszwvqk -d d38vvdankg655o -t -c "update rutor set magnet = replace(magnet, 'rutor.info','videofilms.cf')"
echo "update susses"
