import os
import re
import logging
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from src.data_grabber import get_data
from src.gpt_caller import summary_logic
from src.notion_operate import post_scholar_page

logging.basicConfig(level=logging.INFO)
line_bot_api = LineBotApi(os.getenv("ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default="true").lower() == "true"

def auto_paper_logic(keyword):
    data_list, url_list = get_data(keyword)
    if not data_list:
        return None
    logging.info(f"Successful get data:{url_list}")
    summary_list = summary_logic(data_list=data_list)
    logging.info(f"Successful summarize:{summary_list}")
    res = post_scholar_page(keyword,summary_list,url_list)
    return res

def _check_extract(s):
    matches = re.findall(r'\[(.*?)\]', s)
    return matches[0] if matches else None

app = Flask(__name__)

# domain root
@app.route("/")
def home():
    return "Auto Paper AI is amazing."


@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    link = "https://www.notion.so/AutoScholar-Blog-1750c4545a6d467393294c3b4bdf4867?pvs=4"

    if event.message.type != "text":
        return

    if event.message.text == "工作模式":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=">_<")
        )
        return

    if event.message.text == "休眠模式":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="zzZ")
        )
        return
    
    if working_status and _check_extract(event.message.text):
        logging.info("進入神秘地帶啦")
        keyword = _check_extract(event.message.text)
        logging.info(f"關鍵字是:{keyword}")
        response = auto_paper_logic(keyword=keyword)
        if response == 200:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"您針對{keyword}所執行結果為:{response}，調研結果已由負責的AI完成，請點擊以下連結進行查看:\n{link}"))            
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"您針對{keyword}所執行結果為:{response}，也許您搜索的關鍵字有誤或負責的AI在忙..."))


if __name__ == "__main__":
    app.run()
