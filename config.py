# aToken cookie in the browser site (region does not matter)
# get it from the application tab in the dev tools or from a request in the network profiler
AUTH_TOKEN = "token goes here"

if (AUTH_TOKEN == "token goes here"):
    print("SET YOUR AUTH TOKEN IN config.py BEFORE DOWNLOADING ! ! !")
    exit()

API_DOWNLOAD_URL = "https://cmx-secure.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getUserPurchase"
API_HEADERS = {
    "x-api-version" : "3.9.7",
    "x-client-application" : "com.comixology.comics",
    "x-currency" : "USD_US",
    "x-region" : "US",
    "x-user-token" : "lwa-|" + AUTH_TOKEN
}