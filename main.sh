export PYTHONPATH="${PYTHONPATH}:$(pwd)"

cd scripts
./run-llm.sh & ./web.sh