import re
import openai
import tiktoken
from googletrans import Translator as GoogleTranslator

def _translate_en2zh(english_content):
    if re.search(r"[\u4e00-\u9fff]", english_content):
        return english_content
    translator = GoogleTranslator()
    try:
        translation = translator.translate(english_content, src="en", dest="zh-tw").text
        while translation is None:
            translation = translator.translate(
                english_content, src="en", dest="zh-tw"
            ).text
        return translation
    except Exception as e:
        return f"錯誤翻譯: {e}"

def _call_openai_api(prompt, temperature, max_tokens):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[        
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response["choices"][0]["message"]["content"]

def _count_tokens(content, model= "gpt-3.5-turbo-0613"):
    messages = [
        {
            "role": "user",
            "content": content,
        },
    ]
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def summary_logic(data_list):
    result = []
    for data in data_list:
        if _count_tokens(data) > 11000:
            data = data[:64500]
        prompt = f"""{data}\n以上是某論文內容，你要將重點觀念和內容提到的論點進行摘要，摘要700字即可，中文條列式重點摘要："""
        res = _call_openai_api(prompt=prompt,temperature=0,max_tokens=2500)
        res = _translate_en2zh(res)
        result.append(res)
    return result
