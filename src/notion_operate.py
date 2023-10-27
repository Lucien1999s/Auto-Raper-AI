import os
import json
import requests
import random
from datetime import date
from dotenv import load_dotenv
load_dotenv()

class NotionHelper:
    def _get_today(self):
        today = date.today()
        return today.strftime("%Y-%m-%d")

    def _random_color(self):
        """Random choose color for different paragraph"""
        colors = [
            "red",
            "yellow",
            "blue",
            "green",
            "gray",
            "brown",
            "purple",
            "pink",
            "orange",
            "default",
        ]
        return random.choice(colors)

    def _random_icon(self):
        """Random choose icon"""
        icons = [
            "🧐",
            "🤭",
            "🫠",
            "🫣",
            "🫡",
            "😳",
            "🥳",
            "😝",
            "😘",
            "😉",
        ]
        return random.choice(icons)

    def retrieve_command(self):
        notion_token = os.getenv("NOTION_INTEGRATION_SECRET")
        block_id = os.getenv("BLOCK_ID")
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        url = f"https://api.notion.com/v1/blocks/{block_id}"

        response = requests.get(url=url, headers=headers)
        data = json.loads(response.text)
        if len(data['quote']['rich_text']) == 0:
            return None
        return data['quote']['rich_text'][0]['text']['content']
        
    def reply_command(self, reply_word):
        notion_token = os.getenv("NOTION_INTEGRATION_SECRET")
        block_id = os.getenv("BLOCK_ID")
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        data = {
            "type": "quote",
            "quote": {
                "rich_text": [{
                "type": "text",
                "text": {
                    "content": reply_word+self._random_icon(),
                    "link": None
                },
                }],
                "color": "default"
            }
        }

        response = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=headers, json=data)
        return response.status_code

    def post_scholar_page(self, keyword, data_list, url_list):
        """Post information on the specify page in notion"""
        notion_token = os.getenv("NOTION_INTEGRATION_SECRET")
        page_id = os.getenv("PAGE_ID")
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

        data = {
            "children": [
                {                
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": self._get_today()+f" {keyword}の調研",
                                "link": None
                            }                    
                        }],
                        "color": self._random_color(),
                        "children": [
                            {
                                "object": "block",
                                "type": "paragraph",
                                "paragraph": {
                                    "rich_text": [                            
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": sub_data.replace("-","📌")
                                            },
                                            "annotations": {"color": "default"},
                                        }
                                        for sub_data in data.split('\n')                                                             
                                    ],                                                                                         
                                },
                            }
                            for data in data_list
                        ]+[
                            {
                                "type": "file",
                                "file": {
                                        "caption": [],
                                    "type": "external",
                                    "external": {
                                        "url": url
                                    }
                                }
                            }
                            for url in url_list
                        ]
                    }
                }
            ]
        }
        response = requests.patch(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=headers,
            json=data,
        )
        return response.status_code

if __name__ == "__main__":
    n=NotionHelper()
    print(n.retrieve_command())