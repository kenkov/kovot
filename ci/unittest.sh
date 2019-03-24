set -eu

cd `dirname $0`/..

docker image build -t kovot .
docker container run --entrypoint python3 dialogapi -m unittest discover -v /kovot/test