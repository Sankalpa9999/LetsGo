import hmac
import base64
import hashlib

def generate_esewa_signature(secret_key, data_string):
    """
    Generates HMAC SHA-256 signature, base64 encoded.
    :param secret_key: str
    :param data_string: str (e.g., "total_amount=100,transaction_uuid=123,product_code=EPAYTEST")
    :return: base64 signature
    """
    digest = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=data_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode()
