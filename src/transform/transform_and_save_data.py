import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def transform_and_save_data(event, context):
    logger.info("Lambda function triggered by S3 event")
    # Log the incoming event
    logger.info(f"Received event: {json.dumps(event)}")
    
    # You can add additional processing here
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success! File processed.')
    }
