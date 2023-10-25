from src.data_grabber import Grabber
from src.gpt_caller import LLM
from src.notion_operate import NotionHelper

class BOT:
    def __init__(self):
        self.grabber = Grabber()
        self.llm = LLM()
        self.notionhelper = NotionHelper()
    
    def auto_paper_logic(self, keyword):
        data_list, url_list = self.grabber.get_data(keyword)
        if not data_list:
            return 999
        summary_list = self.llm.summary_logic(data_list=data_list)
        res = self.notionhelper.post_scholar_page(keyword,summary_list,url_list)
        return int(res)

# if __name__ == "__main__":
#     b = BOT()
#     print(b.auto_paper_logic("ninja"))