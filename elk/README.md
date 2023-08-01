# create token
docker exec -it elasticsearch elasticsearch-create-enrollment-token -s kibana
# check the validation passwd
docker logs kibana
# reset passwd
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic