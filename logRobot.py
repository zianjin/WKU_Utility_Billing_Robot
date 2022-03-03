# This Script is Used for WKU Students to Record EveryDay's Water and Electric Fee
import sys
import requests
import datetime, pytz


# Login to Get the Cookie
def auth():
    # Specify the Login Key
    ymToken = 'Your ymToken'
    ymUserId = 'Your ymUserId'
    key = 'ymToken=' + ymToken + '&ymUserId=' + ymUserId
    # Merge into Payload
    payload = key + '&platform=WECHAT_H5&schoolCode=16405'
    # Send the Login Request
    loginUrl = "https://application.xiaofubao.com/app/login/getThirdUserAuthorize"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                      'Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002e)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    response = requests.request("POST", loginUrl, headers=headers, data=payload)
    # Return the Cookies
    return response.cookies




# Function to Request the Remaining Charges of Water
def requestWaterFee(authCookie, areaCode):
    # Specify the Area Info
    waterArea = 'areaCode=&areaId=1912101709517173&'
    result = requestFee(authCookie, waterArea + areaCode)
    return result.get("data").get("amount")


# Function to Request the Remaining Kilowatts of Electricity
def requestElectricFee(authCookie, areaCode):
    # Specify the Area Info
    electricArea = 'areaCode=&areaId=1912101703037172&'
    result = requestFee(authCookie, electricArea + areaCode)
    return result.get("data").get("surplus")


def requestFee(authCookie, areaInfo):
    # Request Basic Info
    url = "https://application.xiaofubao.com/app/electric/queryRoomSurplus"
    # Send the Query Request
    payload = areaInfo + '&platform=YUNMA_WECHAT'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                      'Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002e)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    response = requests.request("POST", url, headers=headers, data=payload, cookies=authCookie)
    return response.json()




# Main Function to Record
if __name__ == '__main__':
    # Get the Login Cookie
    authResult = auth()

    # Get the Room Info
    areaId = sys.argv[1]

    # Request Fee
    record = str(datetime.datetime.now(pytz.timezone('Asia/Shanghai'))) + '\t' \
         + str(requestElectricFee(authCookie=authResult, areaCode=areaId)) + '\t' \
         + str(requestWaterFee(authCookie=authResult, areaCode=areaId)) + '\n'

    # Write into the File
    with open("log_" + areaId + ".txt","a") as file:
        file.write(record)
