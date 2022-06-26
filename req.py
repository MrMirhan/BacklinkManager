from email.mime import base
import requests
import urllib.parse

def base_url(url, with_path=False):
    parsed = urllib.parse.urlparse(url)
    path   = '/'.join(parsed.path.split('/')[:-1]) if with_path else ''
    parsed = parsed._replace(path=path)
    parsed = parsed._replace(params='')
    parsed = parsed._replace(query='')
    parsed = parsed._replace(fragment='')
    return parsed.geturl()

def get_id(url):
    try:
        req = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Timeout 1..")
        return False
    except:
        return False
    try:
        if req.status_code == 200:
            if 'shortlink' in req.links.keys():
                return req.links['shortlink']['url'].split('=').pop()
            elif 'alternate' in req.links.keys():
                return req.links['alternate']['url'].split('/').pop()
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        try:
            print(req.links)
        except:
            pass
        return False

def send_comment(url, id):
    form = dict()
    form["email-notes"] = "email-notes-here"
    form["comment_post_ID"] = str(id)
    form["author"] = "Brian Goldenberg"
    form["email"] = "brian.goldenberg1@gmail.com"
    form["url"] = "https://google.com"
    form["comment"] = "Very greate post thanks.."
    form["comment_parent"] = str(id)
    form["_wp_unfiltered_html_comment"] = "_wp_unfiltered_html_comment"

    settings = {
        "url": base_url(url) + "/wp-comments-post.php",
        "data": form,
        "headers":{
            "mimeType": "multipart/form-data"
        }
    }
    try:
        req = requests.post(settings['url'], data=settings['data'], headers=settings['headers'], timeout=3)
        if req.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print("Timeout 2..")
        return False
    except Exception as e:
        print(e)
        return False

def add_blacklist(url):
    with open("./blacklist2.txt","a") as f:
        if url in blacklist2:
            pass
        else:
            f.write('\n'+url)
        f.close()

#blacklist = [url.replace('\n', '') for url in open('./blacklist.txt', 'r').readlines()]
blacklist2 = [url.replace('\n', '') for url in open('./blacklist2.txt', 'r').readlines()]
urllist = [url.replace('\n', '') for url in open('./urllist.txt', 'r').readlines() if url.replace('\n', '') not in blacklist2]

x = 0
y = 0
for url in urllist:
    x += 1
    uid = get_id(url)
    if not uid == False:
        comment = send_comment(url, uid)
        if comment == False:
            add_blacklist(url)
            print("#",x," | Can not send comment quickliy..")
        else:
            y+=1
            print('#', x, ' - C #',y, '| Successfully commented..\n',url)
    else:
        add_blacklist(url)
        print("#",x," | Can not send comment quickliy..")