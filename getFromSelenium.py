from datetime import datetime
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getFromSelenium(updated_at: datetime):
    # "updated_at": updated_at,
    travelPlanDetailDict = {
        "single": {
            "premier": {
                "chPlanName": "",
                "enPlanName": "",
                "summary": [],
                "detail": [],
                "updated_at": updated_at,
            },
            "select": {
                "chPlanName": "",
                "enPlanName": "",
                "summary": [],
                "detail": [],
                "updated_at": updated_at,
            },
            "cruise": {
                "chPlanName": "",
                "enPlanName": "",
                "summary": [],
                "detail": [],
                "updated_at": updated_at,
            },
        },
        "annual": {
            "premier": {
                "chPlanName": "",
                "enPlanName": "",
                "summary": [],
                "detail": [],
                "updated_at": updated_at,
            },
            "select": {
                "chPlanName": "",
                "enPlanName": "",
                "summary": [],
                "detail": [],
                "updated_at": updated_at,
            },
        },
    }

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://www.bluecross.com.hk/ch/Travel-Smart/Application")

    wait = WebDriverWait(browser, 10)
    try:
        # single-ch
        selectQuoteButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#selectPlan>button"))
        )
        browser.execute_script("window.scrollTo(0, 400)")
        time.sleep(2)
        selectQuoteButton.click()
        travelPlanDetailDict = getSummaryFromHtml(
            browser.page_source, travelPlanDetailDict, False, "single"
        )

        # detail
        moreButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".aia-bx-coverageCom-more"))
        )
        browser.execute_script("window.scrollTo(0, 400)")
        time.sleep(2)
        moreButton.click()
        extraButton = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".aia-bx-quotePage-extra-extend")
            )
        )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        extraButton.click()
        browser.execute_script(
            "document.querySelectorAll('.ant-collapse-expand-icon').forEach((row)=>{setTimeout(()=>{row.click()},0)})"
        )
        time.sleep(2)
        travelPlanDetailDict = getDetailFromHtml(
            browser.page_source, travelPlanDetailDict, False, "single"
        )
        time.sleep(10)

        # single-en
        browser.get(browser.current_url.replace("ch", "en"))
        time.sleep(2)
        travelPlanDetailDict = getSummaryFromHtml(
            browser.page_source, travelPlanDetailDict, True, "single"
        )
        time.sleep(2)

        # detail
        moreButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".aia-bx-coverageCom-more"))
        )
        browser.execute_script("window.scrollTo(0, 400)")
        time.sleep(2)
        moreButton.click()
        extraButton = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".aia-bx-quotePage-extra-extend")
            )
        )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        extraButton.click()
        browser.execute_script(
            "document.querySelectorAll('.ant-collapse-expand-icon').forEach((row)=>{setTimeout(()=>{row.click()},0)})"
        )
        time.sleep(2)
        travelPlanDetailDict = getDetailFromHtml(
            browser.page_source, travelPlanDetailDict, True, "single"
        )
        time.sleep(10)

        # annual-ch
        browser.get("https://www.bluecross.com.hk/ch/Travel-Smart/Application")
        annualButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#tab_allYear"))
        )
        annualButton.click()
        selectQuoteButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#selectPlan>button"))
        )
        browser.execute_script("window.scrollTo(0, 400)")
        time.sleep(2)
        selectQuoteButton.click()
        travelPlanDetailDict = getSummaryFromHtml(
            browser.page_source, travelPlanDetailDict, False, "annual"
        )

        # annual-en
        browser.get(browser.current_url.replace("ch", "en"))
        time.sleep(2)
        travelPlanDetailDict = getSummaryFromHtml(
            browser.page_source, travelPlanDetailDict, True, "annual"
        )
        time.sleep(2)
    except Exception as e:
        print("error")
        browser.save_screenshot("error.png")
        print(e)
    browser.quit()
    return travelPlanDetailDict


def getSummaryFromHtml(
    html: str, travelPlanDetailDict: dict[str, list], isAddEn=False, type="single"
):
    soup = BeautifulSoup(html, "html.parser")
    # plan name
    soupTravelNameRow = soup.select_one("div.aia-bx-quotePage-infoCard-left-title")
    soupPlanNameRows = soup.select(
        "div.aia-bx-quote-coverageCom>div.listItem div.topItemOne"
    )

    if isAddEn:
        planNamePrefix = soupTravelNameRow.text + " - "
        if len(soupPlanNameRows) > 0:
            travelPlanDetailDict[type]["premier"]["enPlanName"] = (
                planNamePrefix + soupPlanNameRows[0].text
            )
        if len(soupPlanNameRows) > 1:
            travelPlanDetailDict[type]["select"]["enPlanName"] = (
                planNamePrefix + soupPlanNameRows[1].text
            )
        if len(soupPlanNameRows) > 2:
            travelPlanDetailDict[type]["cruise"]["enPlanName"] = (
                planNamePrefix + soupPlanNameRows[2].text
            )
    else:
        planNamePrefix = soupTravelNameRow.text + " - "
        if len(soupPlanNameRows) > 0:
            travelPlanDetailDict[type]["premier"]["chPlanName"] = (
                planNamePrefix + soupPlanNameRows[0].text
            )
        if len(soupPlanNameRows) > 1:
            travelPlanDetailDict[type]["select"]["chPlanName"] = (
                planNamePrefix + soupPlanNameRows[1].text
            )
        if len(soupPlanNameRows) > 2:
            travelPlanDetailDict[type]["cruise"]["chPlanName"] = (
                planNamePrefix + soupPlanNameRows[2].text
            )
    # plan detail Rows
    soupPlanDetailRows = soup.select(
        "div.aia-bx-coverageCom-left-collapse>.ant-collapse-item .ant-collapse-header-text"
    )
    detailIndex = -1
    for idx, div in enumerate(soupPlanDetailRows):
        # detailIndex = 0
        soup2 = BeautifulSoup(str(div), "html.parser")
        benefitName = ""
        for idx2, div2 in enumerate(soup2.select("div>div")):
            planKey = ""
            if idx2 == 0:
                detailIndex = detailIndex + 1
                benefitName = "".join(i for i in div2.text if not i.isdigit())
            if idx2 == 1:
                planKey = "premier"
            elif idx2 == 2:
                planKey = "select"
            elif idx2 == 3:
                planKey = "cruise"
            else:
                continue

            if "Optional" in benefitName or "自選" in benefitName:
                detailIndex = detailIndex - 1
                continue

            print(type, planKey, detailIndex, benefitName)
            if idx2 == 1 or idx2 == 2 or idx2 == 3:
                if isAddEn is False:
                    travelPlanDetailDict[type][planKey]["summary"].append(
                        {
                            "chName": benefitName,
                            "price": float(
                                "".join(
                                    i for i in div2.text if (i.isdigit() or i == ".")
                                )
                            ),
                            "currency": "".join(
                                i
                                for i in div2.text
                                if not (i.isdigit() or i == "," or i == ".")
                            ),
                        }
                    )
                else:
                    travelPlanDetailDict[type][planKey]["summary"][detailIndex][
                        "enName"
                    ] = benefitName
    return travelPlanDetailDict


def getDetailFromHtml(
    html: str, travelPlanDetailDict: dict[str, list], isAddEn=False, type="single"
):

    soup = BeautifulSoup(html, "html.parser")

    soupPlanDetailBlocks = soup.select(
        "div.aia-bx-quote-coverageCom div.ant-collapse-item"
    )
    detailIndex = -1
    detailIndex2 = -1
    for idx, div in enumerate(soupPlanDetailBlocks):
        print("idx", idx)
        soup2 = BeautifulSoup(str(div), "html.parser")
        soupPlanMainRow = soup2.select(".ant-collapse-header-text>div>div")
        for idx2, div2 in enumerate(soupPlanMainRow):
            print("idx2", idx2)
            planKey = ""
            if idx2 == 0:
                detailIndex = detailIndex + 1
                benefitName = "".join(
                    s for i, s in enumerate(div2.text) if not (i >= 2 and s.isdigit())
                )
            if idx2 == 1:
                planKey = "premier"
            elif idx2 == 2:
                planKey = "select"
            elif idx2 == 3:
                planKey = "cruise"
            else:
                continue
            if "Optional" in benefitName or "自選" in benefitName:
                detailIndex = detailIndex - 1
                continue

            if idx2 == 1 or idx2 == 2 or idx2 == 3:
                if isAddEn is False:
                    if div2.text == "✔":
                        travelPlanDetailDict[type][planKey]["detail"].append(
                            {
                                "chName": benefitName,
                                "type": "true",
                                "subItems": [],
                            }
                        )
                    elif div2.text == "-":
                        travelPlanDetailDict[type][planKey]["detail"].append(
                            {
                                "chName": benefitName,
                                "type": "N/A",
                                "subItems": [],
                            }
                        )
                    else:
                        travelPlanDetailDict[type][planKey]["detail"].append(
                            {
                                "chName": benefitName,
                                "price": float(
                                    "".join(
                                        i
                                        for i in div2.text
                                        if (i.isdigit() or i == ".")
                                    )
                                ),
                                "currency": "".join(
                                    i
                                    for i in div2.text
                                    if not (i.isdigit() or i == "," or i == ".")
                                ),
                                "subItems": [],
                            }
                        )
                else:
                    travelPlanDetailDict[type][planKey]["detail"][detailIndex][
                        "enName"
                    ] = benefitName

        soupPlanDetailRows = soup2.select(".ant-collapse-content-box>div")
        if "Optional" in soupPlanMainRow[0].text or "自選" in soupPlanMainRow[0].text:
            continue
        else:
            detailIndex2 = detailIndex2 + 1
        for idx3, div3 in enumerate(soupPlanDetailRows):
            soup3 = BeautifulSoup(str(div3), "html.parser")
            for idx4, div4 in enumerate(
                soup3.select("div:has(>div)>div:not(.preBox):not(:first-child)")
            ):
                planKey = ""
                if idx4 == 0:
                    benefitName = "".join(
                        s
                        for i, s in enumerate(div4.text)
                        if not (i >= 2 and s.isdigit())
                    )
                if idx4 == 1:
                    planKey = "premier"
                elif idx4 == 2:
                    planKey = "select"
                elif idx4 == 3:
                    planKey = "cruise"
                else:
                    continue
                if "Optional" in benefitName or "自選" in benefitName:
                    continue
                if idx4 == 1 or idx4 == 2 or idx4 == 3:
                    if isAddEn is False:
                        if div4.text == "✔":
                            travelPlanDetailDict[type][planKey]["detail"][detailIndex2][
                                "subItems"
                            ].append(
                                {
                                    "chName": benefitName,
                                    "type": "true",
                                }
                            )
                        elif div4.text == "-":
                            travelPlanDetailDict[type][planKey]["detail"][detailIndex2][
                                "subItems"
                            ].append(
                                {
                                    "chName": benefitName,
                                    "type": "N/A",
                                }
                            )
                        elif "HK$" in div4.text:
                            travelPlanDetailDict[type][planKey]["detail"][detailIndex2][
                                "subItems"
                            ].append(
                                {
                                    "chName": benefitName,
                                    "price": float(
                                        "".join(
                                            i
                                            for i in div4.text
                                            if (i.isdigit() or i == ".")
                                        )
                                    ),
                                    "currency": "".join(
                                        i
                                        for i in div4.text
                                        if not (i.isdigit() or i == "," or i == ".")
                                    ),
                                }
                            )
                        else:
                            travelPlanDetailDict[type][planKey]["detail"][detailIndex2][
                                "subItems"
                            ].append({"chName": benefitName, "text": div4.text})
                    else:
                        travelPlanDetailDict[type][planKey]["detail"][detailIndex2][
                            "subItems"
                        ][idx3]["enName"] = benefitName
    return travelPlanDetailDict
