import yfinance
from datetime import datetime
from dateutil.relativedelta import relativedelta

def getPrice(ticker, date):
    data = ticker.history(start=date, end=date + relativedelta(days=1),interval="1d", actions=False)
    if len(data) == 0:
        daysback = 1
        while len(data) == 0:
            start=date + relativedelta(days=-1*daysback)
            data = ticker.history(start=start, end=start + relativedelta(days=1),interval="1d", actions=False)
            daysback += 1
    return {
        "date" : data.index[0].strftime("%Y-%m-%d"),
        "price" : (data["High"][0] + data["Low"][0])/2
    }
    

tickerName = input("Enter Ticker Name: ")
if tickerName[-1] == "T":
    tokyoMode = True
else:
    tokyoMode = False
startDateStr = input("Enter Start Date (YYYY-MM-DD): ")
startDate = datetime.strptime(startDateStr, '%Y-%m-%d')
endDateStr = input("Enter End Date (YYYY-MM-DD) default: today: ")
if endDateStr == "":
    endDate = datetime.now()
else:
    endDate = datetime.strptime(endDateStr, '%Y-%m-%d')
buyDay = input("What day will you buy every month default: same as starting date : ")
if buyDay == "":
    buyDay = startDate
else:
    buyDay = startDate.replace(day=int(buyDay))

initialInvestment = int(input("Initial investment: "))
amountperMonth = int(input("How much would you buy per month: "))

ticker = yfinance.Ticker(tickerName)
totalAmountInvested = 0
sharesOwnedDCA = 0
startingPrice = getPrice(ticker, startDate)["price"]
endPrice = getPrice(ticker, endDate)["price"]
currentDate = startDate
balanceDCA = 0
while endDate >= currentDate:
    data = getPrice(ticker, currentDate)
    if totalAmountInvested == 0:
        totalAmountInvested = initialInvestment
        newShares = initialInvestment/data["price"]
        if newShares < 100 and tokyoMode:
            balanceDCA = initialInvestment
            print("{} Can't buy stock, Total Balance Available: {}".format(data["date"], balanceDCA))
        elif newShares >= 100  and tokyoMode:
            buyableShares = newShares//100 * 100
            sharesOwnedDCA += buyableShares
            balanceDCA = (newShares%100) * data["price"]
            print("{} Bought {} shares, Total Balance Available: {}".format(data["date"], buyableShares, balanceDCA))
        else:
            sharesOwnedDCA += newShares
            print("{} Bought {} shares for {}".format(data["date"], newShares, initialInvestment))
        currentDate = buyDay
    else:
        totalAmountInvested += amountperMonth
        if tokyoMode:
            balanceDCA += amountperMonth
            newShares =  balanceDCA/data["price"]
        if newShares < 100 and tokyoMode:
            print("{} Can't buy stock, Total Balance Available: {}".format(data["date"], balanceDCA))
        elif newShares >= 100  and tokyoMode:
            buyableShares = newShares//100 * 100
            sharesOwnedDCA += buyableShares
            balanceDCA = (newShares%100) * data["price"]
            print("{} Bought {} shares, Total Balance Available: {}".format(data["date"], buyableShares, balanceDCA))
        else:
            newShares =  amountperMonth/data["price"]
            sharesOwnedDCA += newShares
            print("{} Bought {} shares for {}".format(data["date"], newShares, amountperMonth))
    
    currentDate = currentDate + relativedelta(months=1)

balanceLS = 0

if tokyoMode:
    sharesOwnedLS = totalAmountInvested/startingPrice
    balanceLS = (sharesOwnedLS%100) * startingPrice
    sharesOwnedLS = ((totalAmountInvested/startingPrice)//100) * 100
else:
    sharesOwnedLS = totalAmountInvested/startingPrice
endPriceDCA = sharesOwnedDCA * endPrice
endPriceLS = sharesOwnedLS * endPrice
print("Total Amount invested {}".format(totalAmountInvested))

print("Balance DCA: {}".format(balanceDCA))
print("Shares DCA: {}".format(sharesOwnedDCA))
print("Price on End Date DCA: {} change: {}%".format(endPriceDCA, (endPriceDCA/totalAmountInvested)*100))

print("Balance LS: {}".format(balanceLS))
print("Shares LS: {}".format(sharesOwnedLS))
print("Price on End Date LS: {} change: {}%".format(endPriceLS, (endPriceLS/totalAmountInvested)*100))