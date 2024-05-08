# LLM Video Timeline Description

## Description

This project is aimed at generating a video timeline description using LLMs. It allows users to generate summary and descriptive timelines for videos, making it easier to navigate through video.

## Project Setup

1. Install Poetry:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository
3. Navigate to the project directory
4. Create environment and Install project dependencies:

   ```bash
   poetry shell
   poetry install
   ```

## Usage

### Running the project for the first time?
1. Run the helper script for deploying LlamaEdge API Server on this machine.
```bash
bash run-llm.sh --interactive
```
2. Follow the instructions appearing on the CLI to complete the setup. When prompted for `Installing WasmEdge ...` the recommended option is `1`(Install the latest version of WasmEdge and wasi-nn_ggml plugin)
3. The script further prompts to enter model number or URL for downloading. When prompted, enter model URL as `https://huggingface.co/SanctumAI/Meta-Llama-3-8B-Instruct-GGUF`
4. Further select the quantization as per the resource availability on the local setup. The recommended option is `11`(meta-llama-3-8b-instruct.Q8_0.gguf)
5. When prompted for the definition of the prompt types select option `2`(llama-3-chat)
6. When prompted for reverse prompt select option `n`
7. When prompted for running mode select option `1`(API Server with Chatbot web app)
8. If there is an existing api-server running, then the script prompts for downloading the latest one. Select any option as per the resource availability.
9. Once all the inputs are given, the script shows a command to start the server. For immediately starting the server, select option `y` else `n`
10. Do keep a note of where `WasmEdge` is installed on the local system. Search for log `WasmEdge Installation at <>` on the CLI.
11. Once the setup is complete, the server can be started any time using the displayed command or the command in the below section.

### Just want to host the model?
1. Start the Agent using wasmedge:

```bash
wasmedge --dir .:. --nn-preload default:GGML:AUTO:meta-llama-3-8b-instruct.Q8_0.gguf llama-api-server.wasm --prompt-template llama-3-chat --model-name meta-llama-3-8b-instruct.Q8_0.gguf --socket-addr 0.0.0.0:8080 --log-prompts --log-stat -c 8192
```
If `wasmedge` is not found, check where wasmedge is installed locally and run the same command with the path information.

## License

This project is licensed under the [MIT License](LICENSE).
