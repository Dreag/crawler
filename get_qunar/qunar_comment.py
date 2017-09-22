import requests
import json
from bs4 import BeautifulSoup

sight_file = open("sight_link.json", "r+", encoding="utf-8")
sight_link = json.load(sight_file)

print(sight_link["水立方"][0])
