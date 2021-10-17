EMAIL = ""
PASSWORD = ""
DEVICE_ID = "f245bb5cce9f2e7fb6bb9b6d7dfe85fa" # don't change

if (EMAIL == "" or PASSWORD == ""):
    print("SET YOUR EMAIL AND PASSWORD IN config.py BEFORE DOWNLOADING ! ! !")
    exit()

API_DOWNLOAD_URL = "https://cmx-secure.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getUserPurchase"
API_ISSUE_URL = "http://digital.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getIssueSummaries"
API_LIST_URL = "https://cmx-secure.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getPurchaseTransactions"

API_HEADERS = {
    "User-Agent": "Comics/3.10.17[3.10.17.310418] Google/10",
    "x-client-application" : "com.comixology.comics"
}
