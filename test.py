import requests
from bs4 import BeautifulSoup

url = "https://software.intel.com/en-us/vtune-amplifier-help-building-and-installing-the-sampling-drivers-for-linux-targets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}
r = requests.get(url,headers=headers)
html = r.text

soup = BeautifulSoup(html,"html.parser")
content = soup.find("div",{"class":"book-page-content  hasFirstSidebar"})
text = content.get_text()

with open("test.txt","w+",encoding="utf-8") as f:
    f.write(text)
print(text)