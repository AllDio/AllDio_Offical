def translation_word(word, model):
    import json
    import requests

    def translate(word):
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
        type = ['auto', 'EN2ZH_CN', 'ZH_CN2EN'][model]
        key = {
            'type': type,
            'i': word,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "ue": "UTF-8",
            "action": "FY_BY_CLICKBUTTON",
            "typoResult": "true"
        }
        response = requests.post(url, data=key)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_reuslt(repsonse):
        result = json.loads(repsonse)
        fanyi = result['translateResult'][-1][-1]['tgt']  # or ['src']
        return fanyi

    fanyi = get_reuslt(translate(word))
    return fanyi


def is_Chinese(question):
    for ch in question:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
