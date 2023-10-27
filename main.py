from src.data_grabber import Grabber
from src.gpt_caller import LLM
from src.notion_operate import NotionHelper
from dotenv import load_dotenv
load_dotenv()

class BOT:
    def __init__(self):
        self.grabber = Grabber()
        self.llm = LLM()
        self.notionhelper = NotionHelper()
    
    def auto_paper_logic(self):
        keyword = self.notionhelper.retrieve_command()
        if keyword is None or "指揮官" in keyword:
            word = "指揮官最近沒有需要我調研的內容呢"
            self.notionhelper.reply_command(word)
            return word
        data_list, url_list = self.grabber.get_data(keyword)
        if not data_list:
            word = "指揮官，您的調研關鍵字人家找不到資料..."
            self.notionhelper.reply_command(word)
            return word
        summary_list = self.llm.summary_logic(data_list=data_list)
        res = self.notionhelper.post_scholar_page(keyword,summary_list,url_list)
        if int(res) == 200:
            word = f"指揮官，麗芙已完成您有關{keyword}的調研委託...今天麗芙沒有拖您後腿吧?"
            self.notionhelper.reply_command(word)
            return word
        else:
            word = "指揮官，麗芙這邊調研出了點問題，您能幫幫我嗎？"
            self.notionhelper.reply_command(word)
            return word

if __name__ == "__main__":
    bot = BOT()
    print(bot.auto_paper_logic())