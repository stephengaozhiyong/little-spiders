import requests

HOME = "https://movie.douban.com/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

home_page = requests.get(HOME)

print(home_page.ok)
print(home_page.reason)
print(home_page.text)
print(home_page.status_code)
