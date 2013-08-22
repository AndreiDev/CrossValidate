def getUserProfile(userName):
    import urllib
    import re

    url = 'https://twitter.com/' + str(userName)
    response = urllib.urlopen(url).read()
    match = re.findall(r'<strong>(.*)</strong> Follow',response)
    if match:
        picAndName = re.findall(r'<img src="(.*)" alt="(.*)" class',response)
        pic = picAndName[0][0]
        name = picAndName[0][1]
        tweets = re.findall(r'<strong>(.*)</strong> Tweets',response)[0].replace(',','')
        following = match[0].replace(',','')
        followers = match[1].replace(',','')
        return [name, pic, tweets, following, followers]
    else: 
        return ''
    