import argparse
import base64
import json
import io
import os

import gradio as gr
from PIL import Image
from advisor import NutritionAdvisor

def create_processor(nutrition_advisor):
    def process(input_img):
        # Convert the NumPy array to an image
        image = Image.fromarray(input_img)

        # Create a BytesIO object to hold the image data
        image_bytes = io.BytesIO()

        # Save the image to BytesIO as JPEG
        image.save(image_bytes, format='JPEG')

        return nutrition_advisor.give_advice(image_bytes.getvalue())

    return process


def main(args):
    # Load the OCR token and Zhipu API key from config.json
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            ocr_token = config["baidu_ocr_token"]
            zhipu_api_key = config["zhipu_ai_apikey"]
    except FileNotFoundError:
        pass

    # Load the OCR token and Zhipu API key from environment variables
    ocr_token = os.getenv("BAIDU_OCR_TOKEN")
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    if args.ocr_token:
        ocr_token = args.ocr_token
    if args.zhipu_api_key:
        zhipu_api_key = args.zhipu_api_key
    if not ocr_token or not zhipu_api_key:
        raise ValueError("Please provide OCR token and Zhipu API key")

    nutrition_advisor = NutritionAdvisor(ocr_token, zhipu_api_key)
    process = create_processor(nutrition_advisor)

    demo = gr.Interface(
        fn=process,
        inputs=[gr.Image(label="上传包装图片")],
        outputs=[gr.Markdown(label="分析结果")],
        title="食品包装营养成分分析模型",
        description="上传食品包装图片，模型将识别图片中的文字，分析营养成分，并提供健康建议。",
        examples=[
            ["./test.png"]
        ]
    )
    demo.launch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Nutrition Advisor Gradio Demo',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Example usage:\n'
                f'python server.py --ocr_token [BAIDU_OCR_TOKEN] --zhipu_api_key [ZHIPU_API_KEY]\n'
                '\n'
                'You can also set the environment variables BAIDU_OCR_TOKEN and ZHIPU_API_KEY instead of passing them as arguments.\n'
    )
    parser.add_argument('--ocr_token', type=str, help='Token for Baidu OCR service.')
    parser.add_argument('--zhipu_api_key', type=str, help='API key for Zhipu AI GLM-4.')
    args = parser.parse_args()
    main(args)
