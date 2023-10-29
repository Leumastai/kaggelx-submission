

import requests
import bs4
import json
import nltk

def get_article_p_tags_from_article_url(article_url, num_skip_tags, headers):
    """
    This function extracts paragraph tags from the article HTML info
    """
    response = requests.get(article_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    
    # get text
    paragraphs = soup.find_all(['p', 'strong', 'em'])

    txt_list = []
    tag_list = []
    
    for p in paragraphs:
        if p.href:
            pass
        else:
            if len(p.get_text()) > 20: # this filters out things that are most likely not part of the core article
                if '•' in p.get_text()[0]: # This excludes any bulletpoints that have been merged into a P tag
                    pass
                else:
                    tag_list.append(p.name)
                    txt_list.append(p.get_text())

    ## This snippet of code deals with duplicate outputs from the html, helps us clean up the data further
    count = 0
    article_p_tag_list = []
    for txt in txt_list:
        if count > num_skip_tags:
            if txt not in article_p_tag_list:
                if len(txt) < 200:
                    article_p_tag_list.append(txt)
                else:
                    temp_list = nltk.sent_tokenize(txt)
                    for tmp in temp_list:
                        article_p_tag_list.append(tmp)
                    
        count += 1
    return article_p_tag_list


def get_text_from_article_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    num_skip_tags = 0
    img_article_url = url

    article_body = get_article_p_tags_from_article_url(img_article_url, num_skip_tags, headers) 

    article_body = " ".join(article_body)
    return article_body

# if input.file_path:
#             # Handle file upload if provided
#             with open(input.file_path.filename, "wb") as buffer:
#                 shutil.copyfileobj(input.file_path.file, buffer)
#                 input_file_path = input.file_path.filename
#                 # You can now process the uploaded file as needed
#         else:

if __name__ == "__main__":
    # https://techcrunch.com/2023/10/24/apple-government-officials-lend-support-to-federal-right-to-repair-law/
    url = "https://edition.cnn.com/travel/united-airlines-economy-class-boarding-new-plan/index.html"
    print(get_text_from_article_url(url))

