import requests

url = "http://127.0.0.1:8000/api/todo/"
headers = {
    "Authorization": "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJha2FzaHMxQGdtYWlsLmNvbSIsIm5hbWUiOiJha2FzaCJ9.wdMFLI_tj6WZAW1L28BI--2XOgHaHqK9qG4MvawVLAQ"

}

response = requests.get(url, headers=headers)

print(response)