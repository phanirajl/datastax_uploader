# Install

```
sudo apt install python3 python3-flask

git clone https://github.com/zvolchak/datastax_uploader.git
```

# Use

#### Start the server

```
cd ./datastax_uploader
./app.py
```

#### Make http requests

```
 curl -k -X POST https://127.0.0.1:8080/
{
  "id": "d7be9560d73211ea9d269f2003e0baa6", 
  "timestamp": "Wed, 05 Aug 2020 09:46:35 GMT", 
  "upload_uri": "https://127.0.0.1:8080/upload/d7be9560d73211ea9d269f2003e0baa6"
}

```

Upload a file (you can use a ./mockfile in the project dir) to a "upload_uri" link proved from the previous POST request.

```
   curl -k -F "file=@/PATH/TO/FILE/datastax_uploader/mockfile" -X PUT https://127.0.0.1:8080/upload/d7be9560d73211ea9d269f2003e0baa6
{
  "download": "https://127.0.0.1:8080/download/d7be9560d73211ea9d269f2003e0baa6", 
  "msg": "Uploaded file d7be9560d73211ea9d269f2003e0baa6"
}
```

Navigate to a "download" link provided in the response to download a file:
https://127.0.0.1:8080/download/d7be9560d73211ea9d269f2003e0baa6
