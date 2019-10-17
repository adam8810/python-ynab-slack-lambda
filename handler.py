from src.lambda_function import lambda_handler
import json

event = {
    'httpMethod': 'POST',
    'body': 'user_id=UC4ATLXCZ&text=din'
}
context = {}

result = lambda_handler(event, context)

print(json.dumps(result, indent=4))
