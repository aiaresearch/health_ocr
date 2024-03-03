import base64
import argparse
import json
import os

import requests
import zhipuai


RECOGNIZE_BASE_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/table"


class NutritionAdvisor:

    """
    A class for providing nutrition advice based on image content recognition and analysis.

    :param ocr_token: Baidu OCR token for image text recognition.
    :type ocr_token: str
    :param zhipu_api_key: Zhipu API key for nutrition analysis.
    :type zhipu_api_key: str

    Example usage:
    >>> advisor = NutritionAdvisor(ocr_token='your_ocr_token', zhipu_api_key='your_zhipu_api_key')
    >>> advice = advisor.give_advice("path/to/image.jpg")
    """

    def __init__(self, ocr_token, zhipu_api_key):
        self.ocr_token = ocr_token
        self.zhipu_client = zhipuai.ZhipuAI(api_key=zhipu_api_key)

    def text_recogize(self, img_bytes):
        """
        Recognizes text from an image represented as bytes.

        :param img_bytes: Bytes representation of the image.
        :type img_bytes: bytes
        :return: Recognized text from the image.
        :rtype: str
        """

        request_url = RECOGNIZE_BASE_URL + "?access_token=" + self.ocr_token

        # Encode image to base64
        img = base64.b64encode(img_bytes).decode('utf-8')

        params = {"image": img}
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.post(request_url, data=params, headers=headers)
        results = response.json()['tables_result'][0]['body']
        item_str = ''.join([res["words"] for res in results]).strip()

        return item_str

    def analyze_nutrition(self, nutritions_str):
        """
        Analyzes nutrition information extracted from text.

        :param nutritions_str: Nutrition information extracted from the image.
        :type nutritions_str: str
        :return: Nutrition analysis results.
        :rtype: str
        """

        response = self.zhipu_client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content": "请你对这个食物营养分析"},
                {"role": "assistant", "content": "当然，请你告诉我这个食物的营养成分表"},
                {"role": "user", "content": "这是一些信息，其中包含了这个食物的营养成分表,请你根据其数据计算每一百克或每一百毫升有多少能量、蛋白质、脂肪、碳水化合物和钠"},
                {"role": "user", "content": '这是这个食物的营养成分表' + nutritions_str},
                {"role": "assistant", "content": "好的"},
                {"role": "user", "content": "然后请你根据这些数据，判断这个食品是不是低糖食品、高蛋白食品和低脂食品。低糖食品的定义是碳水化合物含量需≤5g/100g 或 ≤5g/100mL，高蛋白食品的定义是蛋白质含量需≥12g/100g 或 ≥6g/100mL，低脂肪食品的定义是≤3g/100g 或 ≤1.5g/100mL"},
                {"role": "user", "content": "并请你提供对应的健身建议. 请用 MarkDown 样式输出信息"}
            ],
        )
        return response.choices[0].message.dict()["content"]

    def give_advice(self, img):
        """
        Provide nutrition advice based on the content of an image.

        :param img: Either a file path (str) or a bytes object representing the image.
        :type img: str or bytes
        :return: Nutrition advice based on the recognized content of the image.
        :rtype: str
        :raises ValueError: If the input image is not a valid file path or bytes object,
                            or if the input image is empty.
        """

        if isinstance(img, str):
            img_bytes = open(img, 'rb').read()
        elif isinstance(img, bytes):
            img_bytes = img
        else:
            raise ValueError("Input image should be a file path (str) or a bytes object")

        if not img_bytes:
            raise ValueError("Input image should not be empty")

        nutritions_str = self.text_recogize(img_bytes)
        result = self.analyze_nutrition(nutritions_str)
        return result


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
    img_bytes = open(args.img_path, 'rb').read()
    nutritions_str = nutrition_advisor.text_recogize(img_bytes)
    result = nutrition_advisor.analyze_nutrition(nutritions_str)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        return
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Nutrition Advisor',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Example usage:\n'
                f'python advisor.py --ocr_token [BAIDU OCR TOKEN] --zhipu_api_key [ZHIPU AI API KEY] --img_path path/to/image.png --output path/to/output.txt\n'
                '\n'
                'You can also set the environment variables BAIDU_OCR_TOKEN and ZHIPU_API_KEY instead of passing them as arguments.\n'
                '\n'
                'Note: If --output is not specified, the output will be printed to the console.'
    )
    parser.add_argument('--ocr_token', type=str, help='Token for Baidu OCR service.')
    parser.add_argument('--zhipu_api_key', type=str, help='API key for Zhipu AI GLM-4.')
    parser.add_argument('--img_path', type=str, default="test.png", help='Path to the image file to be processed.')
    parser.add_argument('--output', '-o', type=str, help='Output path for the result. If not specified, the result will be printed to the console.')
    args = parser.parse_args()
    main(args)
