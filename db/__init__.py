from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


# import boto3
# from config import Config

# dynamodb = None

# def init_db(app):
#     global dynamodb
#     if not dynamodb:
#         dynamodb = boto3.resource(
#             'dynamodb',
#             aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
#             aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
#             aws_session_token=app.config['AWS_SESSION_TOKEN'],
#             region_name=app.config['AWS_REGION'],
#             endpoint_url=app.config['DYNAMODB_ENDPOINT_URL']
#         )
        
#         # Check User table exists
#         table_name = 'users'
#         existing_tables = [table.name for table in dynamodb.tables.all()]
        
#         if table_name not in existing_tables:
#             table = dynamodb.create_table(
#                 TableName=table_name,
#                 KeySchema=[
#                     {'AttributeName': 'email', 'KeyType': 'HASH'}
#                 ],
#                 AttributeDefinitions=[
#                     {'AttributeName': 'email', 'AttributeType': 'S'}
#                 ],
#                 ProvisionedThroughput={
#                     'ReadCapacityUnits': 5,
#                     'WriteCapacityUnits': 5
#                 }
#             )
#             table.wait_until_exists()
    
#     return dynamodb