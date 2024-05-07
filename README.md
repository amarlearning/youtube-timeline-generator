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

1. Start the Agent using wasmedge:

```bash
wasmedge --dir .:. --nn-preload default:GGML:AUTO:meta-llama-3-8b-instruct.Q8_0.gguf llama-api-server.wasm --prompt-template llama-3-chat --model-name meta-llama-3-8b-instruct.Q8_0.gguf --socket-addr 0.0.0.0:8080 --log-prompts --log-stat -c 8192
```

## License

This project is licensed under the [MIT License](LICENSE).
