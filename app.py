from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    bucket = data['bucket']
    key = data['key']
    expires_in = data.get('expiresIn', 3600)

    s3 = boto3.client(
        's3',
        endpoint_url='https://s3.us-east-1.wasabisys.com',
        aws_access_key_id=os.environ.get('WASABI_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('WASABI_SECRET_KEY'),
        region_name='us-east-1'
    )

    try:
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )
        return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

