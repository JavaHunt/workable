

import requests
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow

# Set the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

# Create the flow object
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',  # Replace with your client secret file path
    scopes=SCOPES,
    redirect_uri='https://hyperverge.workable.com/backend/api/candidates'
)

# Fetch the authorization URL
authorization_url, _ = flow.authorization_url(
    access_type='offline',
    prompt='consent',
)

# Print the authorization URL and ask the user to visit it
print(f'Please visit this URL to authorize the application: {authorization_url}')

# Fetch the redirected URL after authorization
redirected_url = input('Enter the redirected URL after authorization: ')

# Extract the authorization code from the redirected URL
parsed_url = urlparse(redirected_url)
query_params = parse_qs(parsed_url.query)
authorization_code = query_params.get('code')[0]

# Exchange the authorization code for tokens
flow.fetch_token(authorization_response=redirected_url)
credentials = flow.credentials

# Create a session using the access token
session = requests.Session()
session.headers.update({'Authorization': 'Bearer ' + credentials.token})

# Make a request to the webpage
response = session.get('https://hyperverge.workable.com/backend/api/candidates')
print(response.text)  # Print the response content

print(f'Access Token: {credentials.token}')

print("Headers : \n",response.request.headers)
