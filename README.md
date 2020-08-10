# datastax_uploader

Not a properly working solution.

To get upload ID:

```
curl -X POST https://ow6m3i0zp0.execute-api.us-east-1.amazonaws.com/dev/get_url
```

Not the  "upload_uri" in the response. Make a curl PUT request to that uri to upload an asset:
```
curl -X PUT -k -F "file=./mockfile" https://ow6m3i0zp0.execute-api.us-east-1.amazonaws.com/dev/upload_asset?id=UNIQUE_ID
```
