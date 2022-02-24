EMAIL = ""
PASSWORD = ""
DOMAIN = "com"

if (EMAIL == "" or PASSWORD == ""):
    print("SET YOUR EMAIL AND PASSWORD IN config.py BEFORE DOWNLOADING ! ! !")
    exit()

API_DOWNLOAD_URL = "https://cmx-secure.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getUserPurchase"
API_ISSUE_URL = "https://digital.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getIssueSummaries"
API_LIST_URL = "https://cmx-secure.comixology.com/ios/api/com.iconology.android.Comics/3.9.7/?deviceType=tablet&lang=en&store=US&action=getPurchaseTransactions"

API_MANIFEST_URL = "https://kindle-digital-delivery.amazon.com/delivery/manifest/kindle.ebook/"

API_HEADERS = {
    "User-Agent": "Comics/3.10.17[3.10.17.310418] Google/10",
    "x-client-application" : "com.comixology.comics"
}
