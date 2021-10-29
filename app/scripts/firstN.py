import requests
from datetime import datetime

async def getFirstWallets(timestamp_start, period, cnt=None):
    
    day_start = datetime.fromtimestamp(timestamp_start).timetuple().tm_yday
    timestamp_end = timestamp_start + 86400*period

    queryString = "query balancesByWallet {"

    if cnt >= 1000:
        queryString += f"""
            w0:wallets(orderBy: birth, first: 1000, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"]}}) {{
                id
                dailyBalance(orderBy: timestamp, first: 1000) {{
                    ohmBalance
                    day
                }}
            }}
        """
    else:
        queryString += f"""
            w0:wallets(orderBy: birth, first: {cnt%1000}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"]}}) {{
                id
                dailyBalance(orderBy: timestamp, first: 1000) {{
                    ohmBalance
                    day
                }}
            }}
        """
    for i in range(1,int(cnt/1000)):
        if i > 5:
            break
        else:
            first = 1000
            if cnt/i < 1000:
                first = cnt % 1000
                print(first)
            queryString += f"""
                w{i}:wallets(orderBy: birth, first: {first}, skip: {1000*i}, where: {{address_not_in:["0xfd31c7d00ca47653c6ce64af53c1571f9c36566a","0x0822f3c03dcc24d200aff33493dc08d0e1f274a2"]}}) {{
                    id
                    dailyBalance(orderBy: timestamp, first: 1000) {{
                        ohmBalance
                        day
                    }}
                }}
            """
    queryString += "}"
    # balance before listing
    request = requests.post('https://api.thegraph.com/subgraphs/name/deltax2016/olympus-wallets', json={'query': queryString})
    result = request.json()
    
    days = {}

    for res in result['data']:
        for wallet in result['data'][str(res)]:
            for day in wallet['dailyBalance']:
                if (int(day['day']) >= day_start and int(day['day']) <= (day_start+period)):
                        if not (int(day['day']) in days):
                            days[int(day['day'])] = {}
                            days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                            days[int(day['day'])]['balance'] = int(day['ohmBalance']) / 1000000000
                        else:
                            days[int(day['day'])]['timestamp'] = 1609459200 + 86400*int(day['day'])
                            temp = days[int(day['day'])]['balance']
                            temp += (int(day['ohmBalance'])/ 1000000000)
                            days[int(day['day'])]['balance'] = temp
            

    days_array = []
    real_day = datetime.fromtimestamp(int(timestamp_start)).timetuple().tm_yday
    for i in range(0, real_day+period):
        if i in days:
            days_array.append(days[i])
        else:
            tempDay = {}
            tempDay['timestamp'] = 1609459200 + 86400*int(i)
            if i!= 0:
                tempDay['balance'] = days_array[i-1]['balance']
            else:
                tempDay['balance'] = "0"
            days_array.append(tempDay)


    return days_array[real_day:real_day+period]







