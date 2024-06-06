# LLM Video Timeline Description

## Description

This project is aimed at generating a video timeline description using LLMs. It allows users to generate summary and descriptive timelines for videos, making it easier to navigate through video.

# Demo

https://github.com/sahajsoft/llm-video-timeline-description/assets/9383897/65da6fa1-7029-4548-8ab7-8fd23c8c249a

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

1. Run the helper script for deploying the LlamaEdge API Server on this machine and starting the server:

```bash
sh main.sh
```

The application can be reached at `http://localhost:5443`.

## Usage via Docker

Before you start, ensure your system meets the following minimum requirements to run the project using Docker:

- CPU: 8 cores
- Memory: 12GB
- Disk: 20GB

### Building the Docker Image

First, you have to build the Docker image for the project. Navigate to the project's root directory and run the following command:

```bash
docker build -t llm-video-timeline:dev .
```

### Running the Docker Container

After the image has been built, you can run the Docker container with the following command:

```bash
docker run -p 5443:5443 llm-video-timeline:dev
```

The application can be reached at `http://localhost:5443`.

## Components
- UI
   - Bootstrap and jQuery
- Backend
   - APIs exposed via Flask 
- LLM Agent via LamaEdge
   - LLM model - [SanctumAI/Meta-Llama-3-8B-Instruct-GGUF](https://huggingface.co/SanctumAI/Meta-Llama-3-8B-Instruct-GGUF/)
   - Model exposed over APIs using [LlamaEdge](https://github.com/LlamaEdge/LlamaEdge) 

## Features & Extensions

- [x] User-friendly interface
- [x] Validations on user input
- [x] Easy copy-paste of summary and description

#### Extensions
- [ ] History page - showing past requests
- [ ] More unit and Integration tests
- [ ] Improve response time

## License

This project is licensed under the [MIT License](LICENSE).
