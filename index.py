import asyncio
from flask import Flask

from getFromSelenium import getFromSelenium
from getFromRequestsUrl import getFromRequestsUrl

import motor.motor_asyncio

from model.motor import update_plans, update_prices

from datetime import datetime, timedelta, timezone

# from dotenv import load_dotenv

app = Flask(__name__)

client = motor.motor_asyncio.AsyncIOMotorClient("localhost:27017")
db = client["insurance"]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def is_it_true(value):
    return value.lower() == "true"


@app.get("/bluecross")
async def test():
    # ?adult=1&child=0&isFamily=false&startDate=2024-11-04T00:00:00.000Z&endDate=2024-11-05T00:00:00.000Z&type=single
    # in bluecross frontend, endDate limit to 180 days, package "I" is individual
    # package "S" is couple without children, package "F" is couple with children
    # type=annual with individual only accept adult=1
    # type=single or annual
    updated_at = datetime.now(timezone.utc).astimezone()
    travelPlanDetailDict = getFromSelenium(updated_at)
    print(travelPlanDetailDict)

    planParamList = [
        {"adult": 1, "child": 0, "isFamily": False},
        {"adult": 2, "child": 0, "isFamily": True},
        {"adult": 1, "child": 1, "isFamily": True},
    ]
    typeList = ["single", "annual"]
    for type in typeList:
        # update plans to db
        # first plan
        if (
            "premier" in travelPlanDetailDict[type]
            and len(travelPlanDetailDict[type]["premier"]["summary"]) > 0
        ):
            await update_plans(
                db,
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "premier",
                },
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "premier",
                    **travelPlanDetailDict[type]["premier"],
                },
            )
        # second plan
        if (
            "select" in travelPlanDetailDict[type]
            and len(travelPlanDetailDict[type]["select"]["summary"]) > 0
        ):
            await update_plans(
                db,
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "select",
                },
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "select",
                    **travelPlanDetailDict[type]["select"],
                },
            )
        # third plan
        if (
            "cruise" in travelPlanDetailDict[type]
            and len(travelPlanDetailDict[type]["cruise"]["summary"]) > 0
        ):
            await update_plans(
                db,
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "cruise",
                },
                {
                    "company": "bluecross",
                    "type": type,
                    "plan": "cruise",
                    **travelPlanDetailDict[type]["cruise"],
                },
            )

        # for loop 180 days
        for i in range(180):
            if type == "annual" and i > 0:
                continue

            for planParam in planParamList:
                todayDateTime = datetime.today().strftime("%Y-%m-%d")
                endDateTime = (datetime.today() + timedelta(days=i)).strftime(
                    "%Y-%m-%d"
                )
                startDate = todayDateTime + "T00:00:00.000Z"
                endDate = endDateTime + "T00:00:00.000Z"
                adult: int = planParam["adult"]
                child: int = planParam["child"]
                isFamily: bool = planParam["isFamily"]
                result = getFromRequestsUrl(
                    isFamily, adult, child, type, startDate, endDate
                )
                days = i + 1
                updatePricesCommon = {
                    "company": "bluecross",
                    "type": type,
                    "adult": adult,
                    "child": child,
                    "isFamily": isFamily,
                }

                if type == "single":
                    updatePricesCommon["days"] = days
                if len(result.get("data").get("premiumGroup")) > 0:
                    await update_prices(
                        db,
                        {"plan": "premier", **updatePricesCommon},
                        {
                            "plan": "premier",
                            **updatePricesCommon,
                            "price": result.get("data")
                            .get("premiumGroup")[0]
                            .get("memberPrice"),
                            "updated_at": updated_at,
                        },
                    )
                if len(result.get("data").get("premiumGroup")) > 1:
                    await update_prices(
                        db,
                        {
                            "plan": "select",
                            **updatePricesCommon,
                        },
                        {
                            "plan": "select",
                            **updatePricesCommon,
                            "price": result.get("data")
                            .get("premiumGroup")[1]
                            .get("memberPrice"),
                            "updated_at": updated_at,
                        },
                    )
                if len(result.get("data").get("premiumGroup")) > 2:
                    await update_prices(
                        db,
                        {
                            "plan": "cruise",
                            **updatePricesCommon,
                        },
                        {
                            "plan": "cruise",
                            **updatePricesCommon,
                            "price": result.get("data")
                            .get("premiumGroup")[2]
                            .get("memberPrice"),
                            "updated_at": updated_at,
                        },
                    )
    return "done"
