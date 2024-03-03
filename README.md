# Health OCR Project

## Overview

This project, named "health_ocr," is designed to provide nutrition advice based on the content recognition and analysis of images containing nutritional information.

## Usage

### Installation

Before running the scripts, ensure you have the required dependencies installed. You can install them using:

```bash
pip install -r requirements.txt
```

### Running the Gradio Demo (server.py)

To launch the Gradio interface for nutritional analysis, use the following command:

```bash
python server.py --ocr_token [BAIDU OCR TOKEN] --zhipu_api_key [ZHIPU AI API KEY]
```

Alternatively, you can set the environment variables `BAIDU_OCR_TOKEN` and `ZHIPU_API_KEY` instead of passing them as arguments.

### Running the Nutrition Advisor (advisor.py)

If you want to use the `NutritionAdvisor` class separately, you can run the advisor script with the following command:

```bash
python advisor.py --ocr_token [BAIDU OCR TOKEN] --zhipu_api_key [ZHIPU AI API KEY] --img_path path/to/image.png --output path/to/output.txt
```

As before, you can also set the environment variables `BAIDU_OCR_TOKEN` and `ZHIPU_API_KEY` instead of passing them as arguments.

**Note**: If `--output` is not specified, the result will be printed to the console.

### Hosting the Application with Docker

Run the following command to build the Docker image:

```bash
docker build -t health_ocr .
```

Then run the following command to start the Docker container:

```bash
docker run -p 7860:7860 -e BAIDU_OCR_TOKEN=[BAIDU OCR TOKEN] -e ZHIPU_API_KEY=[ZHIPU AI API KEY] health_ocr
```

Replace `[BAIDU OCR TOKEN]` and `[ZHIPU AI API KEY]` with your actual credentials. This command will start your application inside a Docker container, and it will be accessible on port 7860 of your host machine.

Now, you can access the Gradio interface by visiting [http://localhost:7860](http://localhost:7860) in your web browser.

## Dependencies

- Gradio
- Pillow
- Requests
- ZhipuAI

## Acknowledgments

- Baidu OCR Service: [https://ai.baidu.com/tech/ocr](https://ai.baidu.com/tech/ocr)
- Zhipu AI GLM-4: [https://open.bigmodel.cn](https://open.bigmodel.cn)
