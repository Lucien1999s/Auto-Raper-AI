import os
import requests
import random
from datetime import date
# from dotenv import load_dotenv

# load_dotenv()

def _get_today():
    today = date.today()
    return today.strftime("%Y-%m-%d")

def _random_color():
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


def post_scholar_page(keyword, data_list, url_list):
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
                            "content": _get_today()+f" {keyword}の調研",
                            "link": None
                        }                    
                    }],
                    "color": _random_color(),
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
    data_list = ['- 機器學習是一個快速發展的領域，將計算機科學和統計學結合起來，是人工智能和數據科學的核心。\n- 機器學習的主要問題是如何通過經驗自動改進計算機系統，以及統計、計算和信息理論的基本法則。\n- 目前最廣泛使用的機器學習方法是監督學習，通過訓練數據來改進預測模型的準確性。\n- 深度學習是一種特殊的監督學習方法，通過多層神經網絡來學習複雜的特徵表示，已在計算機視覺和語音識別等領域取得重大突破。\n- 目前還存在許多機器學習的研究機會，如構建終身學習系統、團隊合作的混合主動學習等。\n- 機器學習的應用對隱私和數據所有權提出了挑戰，需要社會進行相應的法律和文化調整。\n- 機器學習的發展將有助於理解神經系統、組織和生物進化等其他類型的學習系統。', '- Computer vision is the field of study that focuses on making computers understand and interpret images and videos.\n- It is related to various disciplines such as neuroscience, machine learning, speech, information retrieval, mathematics, computer science, engineering, physics, biology, robotics, cognitive sciences, and psychology.\n- Object recognition is a major challenge in computer vision, and there are various approaches to tackle it, including generative and discriminative models.\n- Generative models focus on modeling the likelihood and prior of object categories, while discriminative models directly model the decision boundary between different categories.\n- Object categorization faces several challenges, including viewpoint variation, illumination, occlusion, scale, deformation, and background clutter.\n- Historically, object recognition has been approached using single object recognition methods, but recent advancements have focused on using machine learning techniques.\n- Machine learning methods, such as generative and discriminative models, have been used for object recognition, and they involve representation, learning, and recognition stages.\n- Representation involves how to represent an object category, whether using appearance only or location and appearance invariances, and whether using part-based or global representations.\n- Learning involves how to form the classifier given training data, including the choice of likelihood or performance maximization, level of supervision, and handling overfitting.\n- Recognition involves how the classifier is used on novel data, including the use of bag-of-words models and feature detection and representation techniques.\n- One approach to object recognition is one-shot learning, which aims to recognize object categories with only a single example.\n- One-shot learning involves model representation, learning and inferences, evaluation dataset, and application.\n- Discriminative methods, such as boosting, have been used for object detection and recognition.\n- Boosting involves defining a family of weak classifiers and iteratively selecting the best weak classifiers to form a strong classifier.\n- Weak detectors, such as Haar filters and part-based detectors, are used as the weak classifiers in boosting.\n- Object detection and recognition applications include document analysis, medical imaging, robotics, finger prints, surveillance, security, and web searching.', '- 機器學習（Machine Learning）是一種能夠從過去的資料中推測未來並適應新情況的技術，它能夠通過練習不斷提升自己的能力。\n- 機器學習在我們的日常生活中已經變得非常普遍，應用於視頻圖像處理、語音語言處理、機器人控制、醫療分析等領域。\n- 機器學習通常需要大量的數據作為訓練集，並使用不同的算法來訓練模型，如決策樹、線性回歸和神經網絡等。\n- 決策樹是一種常用的分類算法，它通過對訓練數據進行分割來做出預測。\n- 線性回歸是一種用於預測連續數值的模型，它通過找到最佳的線性關係來進行預測。\n- 神經網絡是一種高度參數化的模型，它可以學習從一組點到另一組點的數學映射關係，並通過反向傳播算法進行訓練。\n- 過度擬合是指模型在訓練集上表現良好，但在測試集上表現不佳的情況，這是因為模型過於複雜而無法泛化到新的數據。\n- 欠擬合是指模型在訓練集和測試集上都表現不佳的情況，這是因為模型過於簡單而無法捕捉到數據中的複雜關係。\n- 解決偏差-方差平衡的方法包括增加數據量、調整模型參數、使用交叉驗證等。\n- 機器學習還有許多其他的技術和應用，如無監督學習、正則化、集成學習等，這些都是進一步提升模型性能的方法。\n- 學習更多決策樹和神經網絡的資源包括網上教程、課程和書籍，這些資源可以幫助我們更深入地理解機器學習的原理和應用。', '- 機器學習是人工智慧的一個分支，關注的是從數據中學習的系統的構建和研究。\n- 機器學習是通過使用示例數據或過去的經驗來編程計算機以優化性能準則。\n- 機器學習的目標是開發能夠自動檢測數據中的模式並使用這些模式來預測未來數據或其他感興趣的結果的方法。\n- 模式識別是通過使用計算機算法自動發現數據中的規律性並利用這些規律性來採取行動的領域。\n- 監督學習是根據標記的示例來學習，並且可以用來分類和回歸。\n- 分類是一個有限的標籤集合，可以應用於人臉識別、垃圾郵件檢測、醫學診斷等領域。\n- 回歸是一個實值標籤，可以應用於經濟學、流行病學、汽車/飛機導航等領域。\n- 非監督學習是在沒有標籤的數據上進行學習，可以應用於集群分析、圖像壓縮、生物信息學等領域。\n- 強化學習是通過給予獎勵來學習在特定狀態下採取的行動，可以應用於遊戲、機器人控制等領域。\n- 神經網絡是試圖模仿我們的神經系統的結構和功能，它由神經元和它們之間的連接組成。\n- 神經網絡通過計算和計算答案來處理輸入，並將這些答案作為下一級的輸入。\n- 神經網絡可以是前饋網絡或循環網絡，具有不同的輸入方式和結構。\n- 感知器學習算法是一種調整權重和閾值以使神經元正確分類的方法。\n- 感知器學習算法可以保證在線性可分的情況下收斂到正確的解決方案。\n- 多層網絡可以解決感知器無法解決的非線性問題，如XOR問題。\n- 多層網絡的訓練需要調整每個節點之間的權重和閾值。\n- 機器學習的發展是一個重要的研究領域，可以應用於各種領域，如圖像識別、自然語言處理和智能機器人等。']
    res = post_scholar_page("Machine Learning", data_list)
    print(res)