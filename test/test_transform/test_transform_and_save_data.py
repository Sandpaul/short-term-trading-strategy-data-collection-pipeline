import json
from src.transform.transform_and_save_data import transform_and_save_data

def test_transform_and_save_data():
    # Simulate an S3 event payload
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "test-bucket"
                    },
                    "object": {
                        "key": "test-file.csv"
                    }
                }
            }
        ]
    }

    # Call the Lambda function handler
    result = transform_and_save_data(event, None)

    # Check if the Lambda function returned the expected statusCode
    assert result['statusCode'] == 200

    # Check if the body contains the expected message
    assert json.loads(result['body']) == 'Success! File processed.'
