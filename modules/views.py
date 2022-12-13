import requests

def viewUrl(url, useragent, proxies):
    
    headers = {"User-Agent" : useragent}
    proxies = {"http" : proxies}
    
    try:
        req = requests.get(url, headers=headers, proxies=proxies)
    except Exception as err:
        return False
    if req.status_code == 200:
        return True
    else:
        return False
        # print(bstring.ERROR, "Something went wrong!", req.text)