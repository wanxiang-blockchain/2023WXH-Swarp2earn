import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load your price data
filename="LINK AND UNI"
df = pd.read_csv(f"D:\\swap2earn\\all\\all\\{filename}.csv")
price_A = df['priceA'].values
price_B = df['priceB'].values

# Load timestamps (assuming your CSV contains a 'timestamp' column)
timestamps = pd.to_datetime(df['timestamp'])  # 转换为 datetime 格式

# Calculate spread and mspread for each day
spreads = price_A - price_B
mspreads = np.zeros_like(spreads)
sigmas = np.zeros_like(spreads)

for i in range(1, len(spreads)):
    mspreads[i] = spreads[i] - np.mean(spreads[:i])
    sigmas[i] = np.std(mspreads[:i])
    # print(mspreads[i])
    # print(sigmas[i])

# Define thresholds based on the current day's sigma
    open1 = 1 * sigmas
    open2 = -1 * sigmas
    stop1 = 1.5 * sigmas
    stop2 = -1.5 * sigmas
    close1 = 0.5 * sigmas
    close2 = -0.5 * sigmas

profit_list_A = []
profit_list = []
profit_list_B = []
hold = False
hold_price_A = 0
hold_price_B = 0
hold_state = 0  # 1 (A:long B:short)   -1 (A:short B:long)
cumulative_return_A = 0.0
cumulative_return_B = 0.0
cumulative_return = 0.0
days_open = 0  # Track the number of days the position has been open
money=10000
money_values=[]
# Variables to store trade details
trades = []
current_trade = {}
time=[]

for i in range(len(price_A)):
        if hold == False and i > 1:
            if mspreads[i] >= open1[i] and mspreads[i-1] < open1[i]:
                hold_price_A = price_A[i]
                hold_price_B = price_B[i]
                hold_state = 1
                hold = True
                current_trade = {
                    "entry_time": timestamps[i],
                    "entry_price_A": hold_price_A,
                    "entry_price_B": hold_price_B,
                    "entry_state": hold_state,
                    "exit_time": None,
                    "exit_price_A": None,
                    "exit_price_B": None,
                    "profit": None,
                    "return_A": None,
                    "return_B": None,
                    "return": None,
                    "duration_days": None,
                }

            elif mspreads[i] < open2[i] and mspreads[i-1] >= open2[i]:
                hold_price_A = price_A[i]
                hold_price_B = price_B[i]
                hold_state = -1
                hold = True
                current_trade = {
                    "entry_time": timestamps[i],
                    "entry_price_A": hold_price_A,
                    "entry_price_B": hold_price_B,
                    "entry_state": hold_state,
                    "exit_time": None,
                    "exit_price_A": None,
                    "exit_price_B": None,
                    "profit": None,
                    "return_A": None,
                    "return_B": None,
                    "return": None,
                    "duration_days": None,
                }

        else:
            days_open += 1  # Increment the days the position has been open

            if mspreads[i] >= stop1[i] and mspreads[i-1] < stop1[i] and hold_state == 1:
                profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                return_percentage = 0.5*(return_percentage_A + return_percentage_B)

                money = money +  money * (return_percentage / 100)
                cumulative_return_A += return_percentage_A
                cumulative_return_B += return_percentage_B
                cumulative_return += return_percentage

                current_trade["exit_time"] = timestamps[i]
                current_trade["exit_price_A"] = price_A[i]
                current_trade["exit_price_B"] = price_B[i]
                current_trade["profit"] = profit
                current_trade["return_A"] = return_percentage_A
                current_trade["return_B"] = return_percentage_B
                current_trade["return"] = return_percentage
                current_trade["duration_days"] = days_open
                current_trade["money"] = money
                hold_state = 0
                hold = False
                days_open = 0  # Reset days_open
                trades.append(current_trade)
                money_values.append(money)
                time.append(timestamps[i])
            if mspreads[i] <= stop2[i] and mspreads[i-1] > stop2[i] and hold_state == -1:
                profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                return_percentage = 0.5 * (return_percentage_A + return_percentage_B)
                money = money +  money * (return_percentage/100)
                cumulative_return_A += return_percentage_A
                cumulative_return_B += return_percentage_B
                cumulative_return += return_percentage

                current_trade["exit_time"] = timestamps[i]
                current_trade["exit_price_A"] = price_A[i]
                current_trade["exit_price_B"] = price_B[i]
                current_trade["profit"] = profit
                current_trade["return_A"] = return_percentage_A
                current_trade["return_B"] = return_percentage_B
                current_trade["return"] = return_percentage
                current_trade["duration_days"] = days_open
                current_trade["money"] = money
                hold_state = 0
                hold = False
                days_open = 0  # Reset days_open
                trades.append(current_trade)
                money_values.append(money)
                time.append(timestamps[i])
            if mspreads[i] <= close1[i] and mspreads[i-1] > close1[i] and hold_state == 1:
                profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                return_percentage = 0.5 * (return_percentage_A + return_percentage_B)
                money = money +  money * (return_percentage / 100)
                cumulative_return_A += return_percentage_A
                cumulative_return_B += return_percentage_B

                cumulative_return += return_percentage
                current_trade["exit_time"] = timestamps[i]
                current_trade["exit_price_A"] = price_A[i]
                current_trade["exit_price_B"] = price_B[i]
                current_trade["profit"] = profit
                current_trade["return_A"] = return_percentage_A
                current_trade["return_B"] = return_percentage_B
                current_trade["return"] = return_percentage
                current_trade["duration_days"] = days_open
                current_trade["money"] = money
                hold_state = 0
                hold = False
                days_open = 0  # Reset days_open
                trades.append(current_trade)
                money_values.append(money)
                time.append(timestamps[i])
            if mspreads[i] >= close2[i] and mspreads[i-1] < close2[i] and hold_state == -1:
                profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                return_percentage = 0.5* (return_percentage_A + return_percentage_B)
                money = money +  money * (return_percentage / 100)
                cumulative_return_A += return_percentage_A
                cumulative_return_B += return_percentage_B

                cumulative_return += return_percentage
                current_trade["exit_time"] = timestamps[i]
                current_trade["exit_price_A"] = price_A[i]
                current_trade["exit_price_B"] = price_B[i]
                current_trade["profit"] = profit
                current_trade["return"] = return_percentage
                current_trade["return_A"] = return_percentage_A
                current_trade["return_B"] = return_percentage_B
                current_trade["money"] = money

                current_trade["duration_days"] = days_open
                hold_state = 0
                hold = False
                days_open = 0
                trades.append(current_trade)
                money_values.append(money)
                time.append(timestamps[i])

            # if days_open >= 10:  # Check if the position has been open for more than ten days
            #     # Close the position forcibly
            #     profit = 0  # Assume no profit for forced closure
            #     return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
            #     return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
            #     return_percentage = 0.5 * (return_percentage_A + return_percentage_B)
            #     money = money +  money * (return_percentage / 100)
            #     cumulative_return_A += return_percentage_A
            #     cumulative_return_B += return_percentage_B
            #     cumulative_return += return_percentage
            #
            #     current_trade["exit_time"] = timestamps[i]
            #     current_trade["exit_price_A"] = price_A[i]
            #     current_trade["exit_price_B"] = price_B[i]
            #     current_trade["profit"] = profit
            #     current_trade["return_A"] = return_percentage_A
            #     current_trade["return_B"] = return_percentage_B
            #     current_trade["return"] = return_percentage
            #     current_trade["duration_days"] = days_open
            #     current_trade["money"] = money
            #     hold_state = 0
            #     hold = False
            #     days_open = 0  # Reset days_open
            #     trades.append(current_trade)
            #     money_values.append(money)
            if days_open >= 14:  # Check if the position has been open for more than ten days
        # Close the position forcibly
                if hold_state == 1:
                    profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                    return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                    return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                    return_percentage = 0.5 * (return_percentage_A + return_percentage_B)
                    money = money + money * (return_percentage / 100)
                    cumulative_return_A += return_percentage_A
                    cumulative_return_B += return_percentage_B

                    cumulative_return += return_percentage
                    current_trade["exit_time"] = timestamps[i]
                    current_trade["exit_price_A"] = price_A[i]
                    current_trade["exit_price_B"] = price_B[i]
                    current_trade["profit"] = profit
                    current_trade["return_A"] = return_percentage_A
                    current_trade["return_B"] = return_percentage_B
                    current_trade["return"] = return_percentage
                    current_trade["duration_days"] = days_open
                    current_trade["money"] = money
                    hold_state = 0
                    hold = False
                    days_open = 0  # Reset days_open
                    trades.append(current_trade)
                    money_values.append(money)
                    time.append(timestamps[i])
                elif hold_state == -1:
                    profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                    return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                    return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                    return_percentage = 0.5 * (return_percentage_A + return_percentage_B)
                    money = money + money * (return_percentage / 100)
                    cumulative_return_A += return_percentage_A
                    cumulative_return_B += return_percentage_B

                    cumulative_return += return_percentage
                    current_trade["exit_time"] = timestamps[i]
                    current_trade["exit_price_A"] = price_A[i]
                    current_trade["exit_price_B"] = price_B[i]
                    current_trade["profit"] = profit
                    current_trade["return"] = return_percentage
                    current_trade["return_A"] = return_percentage_A
                    current_trade["return_B"] = return_percentage_B
                    current_trade["money"] = money

                    current_trade["duration_days"] = days_open
                    hold_state = 0
                    hold = False
                    days_open = 0
                    trades.append(current_trade)
                    money_values.append(money)
                    time.append(timestamps[i])



        profit_list.append(cumulative_return)
        profit_list_A.append(cumulative_return_A)
        profit_list_B.append(cumulative_return_B)


for trade in trades:
    print("Entry Time:", trade["entry_time"])
    print("Entry Price A:", trade["entry_price_A"])
    print("Entry Price B:", trade["entry_price_B"])
    print("Entry State:", trade["entry_state"])
    print("Exit Time:", trade["exit_time"])
    print("Exit Price A:", trade["exit_price_A"])
    print("Exit Price B:", trade["exit_price_B"])
    print("Profit:", trade["profit"])
    print("Return_A (%):", trade["return_A"])
    print("Return_B (%):", trade["return_B"])
    print("Return (%):", trade["return"])
    print("Duration (days):", trade["duration_days"])
    print('money:', trade['money'])
    print("-" * 50)


print("Total Cumulative Return_A:", cumulative_return_A, "%")
print("Total Cumulative Return_B:", cumulative_return_B, "%")
print("Total Cumulative Return:", cumulative_return, "%")



# 创建一个空的DataFrame来存储输出结果
output_data = pd.DataFrame(columns=[
    "Entry Time", "Entry Price A", "Entry Price B", "Entry State",
    "Exit Time", "Exit Price A", "Exit Price B", "Profit",
    "Return_A (%)", "Return_B (%)", "Return (%)", "Duration (days)","Money"
])
import pytz

# Print trade details
# 在每笔交易结束后，将输出数据添加到DataFrame
# 在每笔交易结束后，将输出数据添加到DataFrame，并处理日期时间
for trade in trades:
    # 将日期时间转换为不带时区信息的形式
    entry_time = trade["entry_time"].tz_localize(None)
    exit_time = trade["exit_time"].tz_localize(None)

    output_data = output_data._append({
        "Entry Time": entry_time,
        "Entry Price A": trade["entry_price_A"],
        "Entry Price B": trade["entry_price_B"],
        "Entry State": trade["entry_state"],
        "Exit Time": exit_time,
        "Exit Price A": trade["exit_price_A"],
        "Exit Price B": trade["exit_price_B"],
        "Profit": trade["profit"],
        "Return_A (%)": trade["return_A"],
        "Return_B (%)": trade["return_B"],
        "Return (%)": trade["return"],
        "Duration (days)": trade["duration_days"],
        "Money": trade["money"]
    }, ignore_index=True)
#
#
# # # 将DataFrame保存为Excel文件
output_data.to_excel(f"{filename}-money.xlsx", index=False)


# 创建一个包含交易详细信息的DataFrame
plt.figure(figsize=(12, 6))
plt.plot( time,money_values, label="Available Funds (Money)")
plt.xlabel("Time")
plt.ylabel("Available Funds")
plt.legend()
plt.grid(True)
plt.show()
#
# # Plot cumulative returns for A and B
plt.figure(figsize=(12, 6))
plt.plot(range(len(profit_list_A)), profit_list_A, label="Cumulative Return A")
plt.plot(range(len(profit_list_B)), profit_list_B, label="Cumulative Return B")
plt.xlabel("Trade Index")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.grid(True)
plt.show()

# Plot spread and sigma levels
# ... （之前的代码）

# Calculate sigma at each time point


# Plot spread and sigma levels
plt.figure(figsize=(12, 6))
plt.plot(range(len(mspreads)), mspreads, label="MSpread")
plt.axhline(0, color='k', linestyle='--', label="Mean")
plt.plot(0.5 * sigmas, color='g', linestyle='--', label="stop-profit")
plt.plot(-0.5 * sigmas, color='g', linestyle='--')
plt.plot(1 * sigmas, color='b', linestyle='--', label="open")
plt.plot(-1 * sigmas, color='b', linestyle='--')
plt.plot(1.5 * sigmas, color='r', linestyle='--', label="stop-loss")
plt.plot(-1.5 * sigmas, color='r', linestyle='--')
plt.xlabel("Time")
plt.ylabel("Mspread")
plt.legend()
plt.grid(True)
plt.show()
