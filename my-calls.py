import httpx
import uuid

# url = "https://cautious-doodle-pjpjx694jxvcr944-5000.app.github.dev/"
url = "http://localhost:5000/"

response = httpx.get(url)
print(response.status_code)
print(response)

uuid = "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"

response = httpx.get(url)
print(response.status_code)
print(response.text)

mydata = {
    "uuid": "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7",
    "text": "Hello Phil!",
    "param2": "Making a POST request",
    "body": "my own value"
}

# A POST request to the API
response = httpx.post(url + "echo", data=mydata)

# Print the response
print(response.status_code)
print(response.text) 

response = httpx.post(url + "uuid", data=mydata)

print(response.status_code)
print(response.text) 