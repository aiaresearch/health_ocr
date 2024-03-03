import argparse
import base64
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
        inputs=[gr.Image()],
        outputs=[gr.Markdown(label="Advice")],
    )
    demo.launch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Nutrition Advisor Gradio Demo',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Example usage:\n'
                f'python server.py --ocr_token [BAIDU OCR TOKEN] --zhipu_api_key [ZHIPU AI API KEY]\n'
                '\n'
                'You can also set the environment variables BAIDU_OCR_TOKEN and ZHIPU_API_KEY instead of passing them as arguments.\n'
    )
    parser.add_argument('--ocr_token', type=str, help='Token for Baidu OCR service.')
    parser.add_argument('--zhipu_api_key', type=str, help='API key for Zhipu AI GLM-4.')
    args = parser.parse_args()
    main(args)
