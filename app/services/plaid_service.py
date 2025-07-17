# from plaid.api import plaid_api
# from plaid.model.link_token_create_request import LinkTokenCreateRequest
# from plaid.model.products import Products
# from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
# from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
# from plaid.model.transactions_get_request import TransactionsGetRequest
# from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
# from plaid import Configuration, ApiClient
# from datetime import datetime, timedelta
# import os
# from app.config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV
# from plaid.model.country_code import CountryCode

# # Setup configuration
# configuration = Configuration(
#     host=f"https://{PLAID_ENV}.plaid.com",
#     api_key={
#         'clientId': PLAID_CLIENT_ID,
#         'secret': PLAID_SECRET,
#     }
# )

# api_client = ApiClient(configuration)
# client = plaid_api.PlaidApi(api_client)

# async def create_link_token(user_id: str):
#     request = LinkTokenCreateRequest(
#         user=LinkTokenCreateRequestUser(client_user_id=user_id),
#         client_name="SmartFinance AI",
#         products=[Products("transactions")],
#         country_codes=[CountryCode.IN],
#         language="en",
#         redirect_uri=os.getenv("PLAID_REDIRECT_URI")
#     )
#     response = client.link_token_create(request)
#     return response["link_token"]

# async def exchange_public_token(public_token: str):
#     request = ItemPublicTokenExchangeRequest(public_token=public_token)
#     response = client.item_public_token_exchange(request)
#     return response["access_token"], response["item_id"]

# async def fetch_transactions(access_token: str):
#     start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
#     end_date = datetime.now().strftime('%Y-%m-%d')
#     request = TransactionsGetRequest(
#         access_token=access_token,
#         start_date=start_date,
#         end_date=end_date,
#         options=TransactionsGetRequestOptions(count=100)
#     )
#     response = client.transactions_get(request)
#     return response["transactions"]
