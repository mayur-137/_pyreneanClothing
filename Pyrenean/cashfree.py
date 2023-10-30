import requests
def cashfree_handle():
        link_id = "0052"
        url = "https://sandbox.cashfree.com/pg/links/{}".format(link_id)
        print(url)
        
        headers = {
            "accept": "application/json",
            "x-api-version": "2022-09-01",
            "x-client-id": "TEST10048875274ada62a720a9b6c35757884001",
            "x-client-secret": "TEST820409eead5db1fa07b95f96212cb4f2a0650a8"
        }

        response = requests.get(url, headers=headers)

        print(response.text)

cashfree_handle()