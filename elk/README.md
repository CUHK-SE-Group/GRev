# 创建token
docker exec -it elasticsearch elasticsearch-create-enrollment-token -s kibana
# 查看验证码
docker logs kibana
# 重置密码
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic