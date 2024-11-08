# test-apexcompare

## create env

```
mkdir myproject
cd myproject
py -3 -m venv .venv
```

## Activate the environment

```
.venv\Scripts\activate
```

## install

```
pip install -r requirements.txt
```

## run

```
flask --app index --debug run
```

## table

1. 忠意旅遊保 - 標準計劃
Request URL:https://eapp.generali.com.hk/bravoapi21/product/premium
Request Method:POST
payment.promotionCode can be not include
-body
data: {
    "dt":"20241023121152",
    "pn":"EAPP",
    "pl":"TRAVELA22", <--22 為 優越,21 為 標準,23 尊貴
    "payment.promotionCode":"AIMC00CT", <--優惠代碼
    "travel.premiumPlan":"I",
    "travel.isUpgradePA":"N",
    "numTravellers":1,
    "numTravellersIncludeChinaMedical":0,
    "timeStamp":1729656712848
    }
hmac: a45f5dc2895a072e75d3d20f54180168a3bbe701ca1bb732f998ce1cc611899e
{"dt":"20241023024727","pn":"EAPP","pl":"TRAVELA22","payment.promotionCode":"AIMC00CT","travel.premiumPlan":"I","travel.isUpgradePA":"N","numTravellers":1,"numTravellersIncludeChinaMedical":0,"timeStamp":1729666047154}
08a459362cb6dc506343ae0569bcadf1f0db532d8f2fa98110794f2aed772588
or 單次旅遊計劃
data: {"dt":"20241023122138","pn":"EAPP","pl":"TRAVELS23","payment.promotionCode":"AIMC00CT","policy.effectiveDateStart":"2024-10-24","policy.effectiveDateEnd":"2024-10-29","travel.premiumPlan":"I","travel.isUpgradePA":"N","travel.includeCruise":"N","numTravellers":1,"timeStamp":1729657298334}
hmac=export const hmacSha256 = (data, mainKey) => {
  const key = mainKey ? mainKey : CryptoJS.AES.decrypt(
    busiSecKey, 'ACTj4a4589rxPEIW2PoE').toString(CryptoJS.enc.Utf8);
  const hmac = CryptoJS.HmacSHA256(data, key);
	const hmacHex = CryptoJS.enc.Hex.stringify(hmac);
  return hmacHex;
}
-response
{
    "msgCode": 0,
    "msgDesc": {
        "premium": {
            "original": 2580.0,
            "discount": 2580.0
        },
        "levy": 2.58
    }
}
-detail is image and pdf

2. starrinsurance「卓悅遊」旅遊保險
https://apex.starrinsurance.com.hk/ah/fee?DateStart=2024-10-23&DateEnd=2024-10-31&product_id=107&PlanOption=Individual&_curcid=16431
-response(by person)
{371: [{InsType: "adult", InsText: "成人", Fee: 195, Min: "18", Max: "150"},…],…}
371: [{InsType: "adult", InsText: "成人", Fee: 195, Min: "18", Max: "150"},…]
0: {InsType: "adult", InsText: "成人", Fee: 195, Min: "18", Max: "150"}
1: {InsType: "child", InsText: "儿童", Fee: 195, Min: "0", Max: "18"}
372: [{InsType: "adult", InsText: "成人", Fee: 263, Min: "18", Max: "150"},…]
373: [{InsType: "adult", InsText: "成人", Fee: 377, Min: "18", Max: "150"},…]
374: [{InsType: "adult", InsText: "成人", Fee: 1050, Min: "18", Max: "71"},…]
375: [{InsType: "adult", InsText: "成人", Fee: 1700, Min: "18", Max: "71"},…]
376: [{InsType: "adult", InsText: "成人", Fee: 2100, Min: "18", Max: "71"},…]

3. zurich Get "Z" Go+ - 簡易計劃
https://gi.zurich.com.hk/page/public/zh/hk/processAction/update.html?step=TravelPlusProcess:Step1QuickQuote&processUuid=d891bee4-01c8-47fd-a6a9-a0d1388836fe
request: post
_version.358f12a3-71b3-4e6c-922b-f87ec495fe3c: 1729658243023
_version.d891bee4-01c8-47fd-a6a9-a0d1388836fe: 1729658179684
TravelPlus.publicZoneKey: TSPT2
TravelPlus.Customer.memberID: 
TravelPlus.Customer.Proposer.proposerType: Individual
TravelPlus.Product.CoverageSelection.GetZGoCoverage.GetZGoData.noOfAdultQuickQuoteFlexdata: 2
TravelPlus.Product.CoverageSelection.GetZGoCoverage.GetZGoData.noOfJuniorQuickQuoteFlexdata: 1
TravelPlus.Product.CoverageSelection.GetZGoCoverage.GetZGoData.noOfElderlyQuickQuoteFlexdata: 1
TravelPlus.Product.departureDate: 23/10/2024
TravelPlus.Product.returnDate: 30/10/2024
TravelPlus.CampaignData.promoCode: 
TravelPlus.Product.planLevelTable: PlanLevel1
TravelPlus.Product.CoverageSelection.GetZGoCoverage.GetZGoData.riderGetZGoChildBuyBack: 
TravelPlus.Product.optionalRiders: 
TravelPlus.Product.optionalRiders: 
TravelPlus.Product.optionalRiders: 
response:
html

4. axa
https://www.axa.com.hk/api/travel-insurance-protection/quotation
post
[{"channel":"B2B2C","cover":"SINGLE","startDate":"2024-10-23","endDate":"2024-10-31","noOfInsuredAdults":3,"noOfInsuredChildrenWithInsuredGuardian":0,"noOfInsuredChildrenWithoutInsuredGuardian":0,"riders":[],"agentId":"04822","travelType":"Return","partyType":"individual","plan":"SILVER"},{"channel":"B2B2C","cover":"SINGLE","startDate":"2024-10-23","endDate":"2024-10-31","noOfInsuredAdults":3,"noOfInsuredChildrenWithInsuredGuardian":0,"noOfInsuredChildrenWithoutInsuredGuardian":0,"riders":[],"agentId":"04822","travelType":"Return","partyType":"individual","plan":"GOLD"},{"channel":"B2B2C","cover":"SINGLE","startDate":"2024-10-23","endDate":"2024-10-31","noOfInsuredAdults":3,"noOfInsuredChildrenWithInsuredGuardian":0,"noOfInsuredChildrenWithoutInsuredGuardian":0,"riders":[],"agentId":"04822","travelType":"Return","partyType":"individual","plan":"PLATINUM"}]
response
0
: 
{plan: "SILVER_SINGLE", premium: 957.21, levy: 0.96, levyRate: 0.001, chargesSum: 0.96, currency: "",…}
1
: 
{plan: "GOLD_SINGLE", premium: 1431.98, levy: 1.43, levyRate: 0.001, chargesSum: 1.43, currency: "",…}
2
: 
{plan: "PLATINUM_SINGLE", premium: 1674.47, levy: 1.67, levyRate: 0.001, chargesSum: 1.67,…}

5. bluecross
https://www.bluecross.com.hk/ch/TravelSmartPlus/CalculatePremium
post add productList: ["TSN", "MTN", "TAN"]
request
{"appNo":"","batchAppNo":"","productCode":"TSN","startDate":"2024-11-04T00:00:00.000Z","endDate":"2024-11-11T00:00:00.000Z","coveredDays":0,"clientType":"","package":"I","individual":1,"adult":0,"child":0,"plan":"","promoCode":"","paUnit":0,"isUpsell":true}
response
code: 0
data: {,…}
premiumGroup: [{seq: 0, appNo: null, productCode: "TSN", plan: null, planCode: "P5", originalPrice: 445,…},…]
premiumGroupForUpsell: [{seq: 3, appNo: null, productCode: "TAN", plan: null, planCode: "PA", originalPrice: 2080,…},…]
errors: null
message: "Request Success"
success: true
