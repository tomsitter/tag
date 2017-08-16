import requests

url = 'http://localhost:5000/upload'
files = {'image': open(r'C:\Users\SAFHT_AdminTom\Pictures\tellaro.jpg', 'rb')}
values = {'title': 'tellaro', 'description': 'Great View!'}
r = requests.post(url, files=files, data=values)
assert 'Success' in r.json().keys()


files = {'image': open(r'C:\Users\SAFHT_AdminTom\Pictures\f9582fb427074e2a85fafad346b4826b.jpg', 'rb')}
values = {'title': 'leaf', 'description': 'So weird'}
r = requests.post(url, files=files, data=values)
assert 'Success' in r.json().keys()

url = 'http://localhost:5000/all'
r = requests.get(url)

'''
[
  {
    "description": "Great View!",
    "filename": "tellaro.jpg",
    "id": 1,
    "latitude": None,
    "longitude": None,
    "title": "tellaro"
  },
  {
    "description": "So weird",
    "filename": "f9582fb427074e2a85fafad346b4826b.jpg",
    "id": 2,
    "latitude": None,
    "longitude": None,
    "title": "leaf"
  }
]
'''
assert len(r.json()) == 2