#!/bin/bash
#
# Helper script for deploying LlamaEdge API Server with a single Bash command
#
# - Works on Linux and macOS
# - Supports: CPU, CUDA, Metal, OpenCL
# - Can run GGUF models from https://huggingface.co/second-state/
#

set -e

# required utils: curl
if ! command -v curl &> /dev/null; then
    printf "[-] curl not found\n"
    exit 1
fi

# parse arguments
port=8080
repo=""
wtype=""
backend="cpu"
ctx_size=512
n_predict=1024
n_gpu_layers=100

# if macOS, use metal backend by default
if [[ "$OSTYPE" == "darwin"* ]]; then
    backend="metal"
elif command -v nvcc &> /dev/null; then
    backend="cuda"
fi

gpu_id=0
n_parallel=8
n_kv=4096
verbose=0
log_prompts=0
log_stat=0
model=""
ggml_version="latest"


ss_urls=(
    "https://huggingface.co/SanctumAI/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/meta-llama-3-8b-instruct.Q8_0.gguf"
)

# sample models
ss_models=(
    "SanctumAI/Meta-Llama-3-8B-Instruct-GGUF"
)

# prompt types
prompt_types=(
    "llama-3-chat"
)


# * install WasmEdge + wasi-nn_ggml plugin
printf "[+] Installing WasmEdge with wasi-nn_ggml plugin ...\n\n"

if curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/5b7a8deaacc1382d77676537daeb93fc9db8c756/utils/install_v2.sh | bash -s -- -v 0.13.5 --rustls; then
    source $HOME/.wasmedge/env
    wasmedge_path=$(which wasmedge)
    printf "\n    The WasmEdge Runtime is installed in %s.\n\n" "$wasmedge_path"
else
    echo "Failed to install WasmEdge"
    exit 1
fi

printf "\n"

# * download meta-llama-3-8b-instruct.Q8_0.gguf
ss_url="https://huggingface.co/SanctumAI/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/meta-llama-3-8b-instruct.Q8_0.gguf"
wfile=$(basename "$ss_url")
if [ -f "$wfile" ]; then
    printf "[+] Using cached model %s \n" "$wfile"
else
    printf "[+] Downloading %s ...\n" "$ss_url"

    # download the weights file
    curl -o "$wfile" -# -L "$ss_url"
fi

# * download llama-api-server.wasm
wasm_url="https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-api-server.wasm"
wasmfile=$(basename "$wasm_url")
if [ -f "$wasmfile" ]; then
    printf "[+] Using cached file %s \n" "$wasmfile"
else
    printf "[+] Downloading %s ...\n" "$wasm_url"

    # download the weights file
    curl -o "$wasmfile" -# -L "$wasm_url"
fi


# * download chatbot-ui
if [ ! -d "chatbot-ui" ]; then
    printf "[+] Downloading Chatbot web app ...\n"
    files_tarball="https://github.com/second-state/chatbot-ui/releases/latest/download/chatbot-ui.tar.gz"
    curl -LO $files_tarball
    if [ $? -ne 0 ]; then
        printf "    \nFailed to download ui tarball. Please manually download from https://github.com/second-state/chatbot-ui/releases/latest/download/chatbot-ui.tar.gz and unzip the "chatbot-ui.tar.gz" to the current directory.\n"
        exit 1
    fi
    tar xzf chatbot-ui.tar.gz
    rm chatbot-ui.tar.gz
    printf "\n"
else
    printf "[+] Using cached Chatbot web app. Skipping download.\n"
fi

# * start llama-api-server
cmd="wasmedge --dir .:. --nn-preload default:GGML:AUTO:meta-llama-3-8b-instruct.Q8_0.gguf llama-api-server.wasm -p llama-3-chat -c 8192 --model-name meta-llama-3-8b-instruct --socket-addr 0.0.0.0:${port} --log-prompts --log-stat"

printf "[+] Will run the following command to start the server:\n\n"
printf "    %s\n\n" "$cmd"
printf "    Chatbot web app can be accessed at http://0.0.0.0:%s after the server is started\n\n\n" "$port"
printf "*********************************** LlamaEdge API Server ********************************\n\n"
eval $cmd

exit 0