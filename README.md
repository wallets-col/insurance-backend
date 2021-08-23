# insurance-backend

## Hacer deploy desde la linea de comando

### ¡¡¡ IMPORTANTE tener cuidado con las keys de las cuentas, antes de hacer deploy ejecutar un aws s3 ls para saber en que cuenta estamos conectados !!!

## PROD

`sam deploy --template-file template.yaml --region us-east-1 --s3-bucket sam-local-development --capabilities CAPABILITY_IAM --stack-name insurance-sam-prod --parameter-overrides EnvironmentValue=prod`

## DEV

`sam deploy --template-file template.yaml --region us-east-1 --s3-bucket sam-local-development --capabilities CAPABILITY_IAM --stack-name insurance-sam-dev --parameter-overrides EnvironmentValue=dev`


# Uso del API

## Endpoint base para produccion

`https://lnw0tmrts2.execute-api.us-east-1.amazonaws.com/prod`

## Endpoint base para desarrollo

`https://kcb4j8nmvf.execute-api.us-east-1.amazonaws.com/dev`

## Uso del API con Postman

El archivo json se lo da el arquitecto



# Tutoriales

## Encriptación con kms

https://gist.github.com/nmarley/99cec84a0b1b9fd87d3ae51c88d68fbb

```python
kms_client = boto3.client("kms")

stuff = kms_client.encrypt(
    KeyId=os.environ["KMS_ARN"],
    Plaintext="secure Text"
)
print(stuff)

"""
{"CiphertextBlob": b"\x01\x02\x02\x00xMH\x82\xb1\x0e\x15\x8a\x98.\x07K\x8aH\x13\xe1\xd6)q\xd3\xaa\x18\x17\xc5}\x07\xafp\xce\xa5:\xa3z\x01X\xc5/\x87\xa0@\x9c\x083tu\xaa\xddH\xe0L\x00\x00\x00i0g\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0Z0X\x02\x01\x000S\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\x1a7\xe4\x81\x7f\xad5(QMy\xe3\x02\x01\x10\x80&il&\x12n>\xd9\x9f\x1f\x08}\xe0i\x9a\xa3\x1bw\xa1"\xb3\xed\xee\xfd\xa1t\x84\xc0\x7f\xab\x95\xfc\x9f2_\x7f\xbfb\x81", "KeyId": "arn:aws:kms:us-east-1:545930365694:key/cbdb5df0-716d-4774-91e9-b7de3ba2bf59", "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "ResponseMetadata": {"RequestId": "b51e1e92-57a1-4d1f-a9fe-06d628104ce2", "HTTPStatusCode": 200, "HTTPHeaders": {"x-amzn-requestid": "b51e1e92-57a1-4d1f-a9fe-06d628104ce2", "cache-control": "no-cache, no-store, must-revalidate, private", "expires": "0", "pragma": "no-cache", "date": "Wed, 12 Aug 2020 16:17:00 GMT", "content-type": "application/x-amz-json-1.1", "content-length": "369"}, "RetryAttempts": 0}}
"""

binary_encrypted = stuff[u"CiphertextBlob"]
print(binary_encrypted)

"""
b"\x01\x02\x02\x00xMH\x82\xb1\x0e\x15\x8a\x98.\x07K\x8aH\x13\xe1\xd6)q\xd3\xaa\x18\x17\xc5}\x07\xafp\xce\xa5:\xa3z\x01X\xc5/\x87\xa0@\x9c\x083tu\xaa\xddH\xe0L\x00\x00\x00i0g\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0Z0X\x02\x01\x000S\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\x1a7\xe4\x81\x7f\xad5(QMy\xe3\x02\x01\x10\x80&il&\x12n>\xd9\x9f\x1f\x08}\xe0i\x9a\xa3\x1bw\xa1"\xb3\xed\xee\xfd\xa1t\x84\xc0\x7f\xab\x95\xfc\x9f2_\x7f\xbfb\x81"
"""

encrypted_base64 = base64.b64encode(binary_encrypted)
print(encrypted_base64)

"""
b"AQICAHhNSIKxDhWKmC4HS4pIE+HWKXHTqhgXxX0Hr3DOpTqjegFYxS+HoECcCDN0dardSOBMAAAAaTBnBgkqhkiG9w0BBwagWjBYAgEAMFMGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMGjfkgX+tNShRTXnjAgEQgCZpbCYSbj7Znx8IfeBpmqMbd6Eis+3u/aF0hMB/q5X8nzJff79igQ=="
"""

print(encrypted_base64.decode())

"""
AQICAHhNSIKxDhWKmC4HS4pIE+HWKXHTqhgXxX0Hr3DOpTqjegFYxS+HoECcCDN0dardSOBMAAAAaTBnBgkqhkiG9w0BBwagWjBYAgEAMFMGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMGjfkgX+tNShRTXnjAgEQgCZpbCYSbj7Znx8IfeBpmqMbd6Eis+3u/aF0hMB/q5X8nzJff79igQ==
"""

binary_data = base64.b64decode(encrypted_base64)
print(binary_data)

"""
b"\x01\x02\x02\x00xMH\x82\xb1\x0e\x15\x8a\x98.\x07K\x8aH\x13\xe1\xd6)q\xd3\xaa\x18\x17\xc5}\x07\xafp\xce\xa5:\xa3z\x01X\xc5/\x87\xa0@\x9c\x083tu\xaa\xddH\xe0L\x00\x00\x00i0g\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0Z0X\x02\x01\x000S\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\x1a7\xe4\x81\x7f\xad5(QMy\xe3\x02\x01\x10\x80&il&\x12n>\xd9\x9f\x1f\x08}\xe0i\x9a\xa3\x1bw\xa1"\xb3\xed\xee\xfd\xa1t\x84\xc0\x7f\xab\x95\xfc\x9f2_\x7f\xbfb\x81"
"""

meta = kms_client.decrypt(CiphertextBlob=binary_data)
print(meta)

"""
{"KeyId": "arn:aws:kms:us-east-1:545930365694:key/cbdb5df0-716d-4774-91e9-b7de3ba2bf59", "Plaintext": b"secure Text", "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "ResponseMetadata": {"RequestId": "3d909ee4-1d90-4ca4-91c4-0584db85e12b", "HTTPStatusCode": 200, "HTTPHeaders": {"x-amzn-requestid": "3d909ee4-1d90-4ca4-91c4-0584db85e12b", "cache-control": "no-cache, no-store, must-revalidate, private", "expires": "0", "pragma": "no-cache", "date": "Wed, 12 Aug 2020 16:17:00 GMT", "content-type": "application/x-amz-json-1.1", "content-length": "160"}, "RetryAttempts": 0}}
"""

plaintext = meta[u"Plaintext"]
print(plaintext)

"""
b"secure Text"
"""

print(plaintext.decode())

"""
secure Text
"""

```
