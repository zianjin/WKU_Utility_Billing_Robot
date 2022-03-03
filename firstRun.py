# This Script is Used for WKU Students to Initialize Utility Billing Robot
import requests
import datetime


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




# Function to Request Area Code
def requestAreaCode(authCookies):
    # Switch to BUILDING Query
    areaCode = 'areaId=1912101709517173'
    buildingList = requestAreaData("queryBuilding", authCookies, areaCode)
    # Output the List
    for index in range(len(buildingList)):
        print(index, buildingList[index].get("buildingName"), sep=': ')
    # Analysis the Input
    userInput = int(input("Building Index: "))
    buildingCode = buildingList[userInput].get("buildingCode")
    areaCode = areaCode + '&buildingCode=' + str(buildingCode)

    # Switch to FLOOR Query
    floorList = requestAreaData("queryFloor", authCookies, areaCode)
    # Output the List
    for index in range(len(floorList)):
        print(index, floorList[index].get("floorName"), sep=': ')
    # Analysis the Input
    userInput = int(input("Floor Index: "))
    floorCode = floorList[userInput].get("floorCode")
    areaCode = areaCode + '&floorCode=' + str(floorCode)

    # Switch to ROOM Query
    roomList = requestAreaData("queryRoom", authCookies, areaCode)
    # Output the List
    for index in range(len(roomList)):
        print(index, roomList[index].get("roomName"), sep=': ')
    # Analysis the Input
    userInput = int(input("Room Index: "))
    roomCode = roomList[userInput].get("roomCode")
    areaCode = areaCode + '&roomCode=' + str(roomCode)
    # Return the areaCode
    return areaCode


def requestAreaData(addOnUrl, authCookie, areaInfo):
    # Merge the Area Info
    payload = 'platform=YUNMA_WECHAT'
    if len(areaInfo) != 0:
        payload = areaInfo + '&' + payload
    url = "https://application.xiaofubao.com/app/electric/" + addOnUrl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                      'Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002e)',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    # Send the Request
    response = requests.request("POST", url, headers=headers, data=payload, cookies=authCookie)
    # Get the List
    return response.json().get("rows")




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

    # Specify the Area Code
    areaId = requestAreaCode(authResult)
    print("Your Area Code is:", areaId)

    # Request Fee
    print(datetime.datetime.now(),
          "\tRemaining Kilowatts: ", requestElectricFee(authCookie=authResult, areaCode=areaId),
          "\tRemaining Water Charges: ", requestWaterFee(authCookie=authResult, areaCode=areaId), sep="")
