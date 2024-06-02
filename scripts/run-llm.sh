#!/bin/bash
#
# Helper script for deploying LlamaEdge API Server with a single Bash command
#
# - Works on Linux and macOS
# - Supports: CPU, CUDA, Metal, OpenCL
# - Can run GGUF models from https://huggingface.co/second-state/
#

set -e

# required utils: curl, git, make
if ! command -v curl &> /dev/null; then
    printf "[-] curl not found\n"
    exit 1
fi
if ! command -v git &> /dev/null; then
    printf "[-] git not found\n"
    exit 1
fi
if ! command -v make &> /dev/null; then
    printf "[-] make not found\n"
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
# 0: server mode
# 1: local mode
# mode=0
# 0: non-interactive
# 1: interactive
interactive=0
model=""
# ggml version: latest or bxxxx
ggml_version="latest"

function print_usage {
    printf "Usage:\n"
    printf "  ./run-llm.sh [--port]\n\n"
    printf "  --model:        model name\n"
    printf "  --interactive:  run in interactive mode\n"
    printf "  --port:         port number, default is 8080\n"
    printf "  --ggml-version: ggml version, default is latest\n"
    printf "Example:\n\n"
    printf '  bash <(curl -sSfL 'https://code.flows.network/webhook/iwYN1SdN3AmPgR5ao5Gt/run-llm.sh')"\n\n'
}

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --model)
            model="$2"
            shift
            shift
            ;;
        --interactive)
            interactive=1
            shift
            ;;
        --port)
            port="$2"
            shift
            shift
            ;;
        --ggml-version)
            ggml_version="$2"
            shift
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $key"
            print_usage
            exit 1
            ;;
    esac
done

# available weights types
wtypes=("Q2_K" "Q3_K_L" "Q3_K_M" "Q3_K_S" "Q4_0" "Q4_K_M" "Q4_K_S" "Q5_0" "Q5_K_M" "Q5_K_S" "Q6_K" "Q8_0")

wfiles=()
for wt in "${wtypes[@]}"; do
    wfiles+=("")
done

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

if [ "$interactive" -eq 0 ]; then

    printf "\n"
    # * install WasmEdge + wasi-nn_ggml plugin
    printf "[+] Installing WasmEdge with wasi-nn_ggml plugin ...\n\n"

    if [ "$ggml_version" = "latest" ]; then
        if curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/5b7a8deaacc1382d77676537daeb93fc9db8c756/utils/install_v2.sh | bash -s -- -v 0.13.5 --rustls; then
            source $HOME/.wasmedge/env
            wasmedge_path=$(which wasmedge)
            printf "\n    The WasmEdge Runtime is installed in %s.\n\n" "$wasmedge_path"
        else
            echo "Failed to install WasmEdge"
            exit 1
        fi
    else
        ggml_plugin="wasi_nn-ggml-$ggml_version"
        if curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -v 0.13.5 --plugins $ggml_plugin wasmedge_rustls; then
            source $HOME/.wasmedge/env
            wasmedge_path=$(which wasmedge)
            printf "\n    The WasmEdge Runtime is installed in %s.\n\n" "$wasmedge_path"
        else
            echo "Failed to install WasmEdge"
            exit 1
        fi
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
    printf "[+] Downloading the latest llama-api-server.wasm ...\n"
    curl -LO https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-api-server.wasm
    printf "\n"

    # * download chatbot-ui
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

    # * start llama-api-server
    cmd="wasmedge --dir .:. --nn-preload default:GGML:AUTO:meta-llama-3-8b-instruct.Q8_0.gguf llama-api-server.wasm -p llama-3-chat -c 8192 --model-name meta-llama-3-8b-instruct --socket-addr 0.0.0.0:${port} --log-prompts --log-stat"

    printf "[+] Will run the following command to start the server:\n\n"
    printf "    %s\n\n" "$cmd"
    printf "    Chatbot web app can be accessed at http://0.0.0.0:%s after the server is started\n\n\n" "$port"
    printf "*********************************** LlamaEdge API Server ********************************\n\n"
    eval $cmd
else
    echo "Invalid value for interactive"
fi

exit 0