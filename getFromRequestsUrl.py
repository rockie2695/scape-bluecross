import requests


def getFromRequestsUrl(
    isFamily=False,
    adult=1,
    child=0,
    type="single",
    startDate="2024-11-04T00:00:00.000Z",
    endDate="2024-11-10T00:00:00.000Z",
):
    if child > 9:
        return "error"
    if isFamily is False and child > 0:
        return "error"
    if isFamily is True and child <= 0 and adult != 2:
        return "error"
    if isFamily is True and child > 0 and (adult > 2 or adult <= 0):
        return "error"
    if type == "annual" and adult != 1 and isFamily is False:
        return "error"

    requestsBodyJson = {
        "batchAppNo": "",
        "coveredDays": 0,
        "clientType": "",
        "plan": "",
        "promoCode": "",
        "paUnit": 0,
        "isUpsell": True,
        "isSpecialRole": False,
        "isShopback": False,
        "productList": ["TSN", "MTN", "TAN"],
        "appNo": "",
        "paUnits": [],
    }
    if child > 0:  # family with children
        requestsBodyJson["package"] = "F"
        requestsBodyJson["individual"] = 0
        requestsBodyJson["adult"] = adult
        requestsBodyJson["child"] = child
    elif isFamily is True and child == 0:  # family without children
        requestsBodyJson["package"] = "S"
        requestsBodyJson["individual"] = 0
        requestsBodyJson["adult"] = adult
        requestsBodyJson["child"] = child
    else:  # individual
        requestsBodyJson["package"] = "I"
        requestsBodyJson["individual"] = adult
        requestsBodyJson["adult"] = 0
        requestsBodyJson["child"] = 0

    if type == "single":
        requestsBodyJson["productCode"] = "TSN"
        requestsBodyJson["startDate"] = startDate
        requestsBodyJson["endDate"] = endDate
    else:
        requestsBodyJson["productCode"] = "TAN"
        requestsBodyJson["startDate"] = startDate

    try:
        r = requests.post(
            "https://www.bluecross.com.hk/ch/TravelSmartPlus/CalculatePremium",
            json=requestsBodyJson,
        )
        if r.status_code == requests.codes.ok:
            test = r.json()
            return test
        else:
            return "error"
    except Exception as e:
        print(e)
        return "error"
