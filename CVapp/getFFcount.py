def getFFcount(userName):
    import urllib
    import re

    url = 'https://twitter.com/' + str(userName)
    response = urllib.urlopen(url).read()
    match = re.findall(r'<strong>(.*)</strong> Follow',response)
    return [match[0].replace(',',''), match[1].replace(',','')]
    