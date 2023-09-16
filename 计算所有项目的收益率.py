import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Specify the folder containing your CSV files
folder_path = "D:\\swap2earn\\all\\all\\"

total_cumulative_return = 0
total_trades = 0
winning_trades = 0  # 用于跟踪胜利交易的数量

# Lists to store results for each file
file_names = []
cumulative_returns_A = []
cumulative_returns_B = []
cumulative_returns = []
win_rates = []
total_trade_numbers = []

# Loop through CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Load the CSV file
        print(filename)
        df = pd.read_csv(os.path.join(folder_path, filename))
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
        win = 0
        all_trades = 0
        trade_all = 0
        # Variables to store trade details
        trades = []
        current_trade = {}
        time = []

        for i in range(len(price_A)):
            if hold == False and i > 1:
                if mspreads[i] >= open1[i] and mspreads[i - 1] < open1[i]:
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
                    trade_all += 1

                elif mspreads[i] < open2[i] and mspreads[i - 1] >= open2[i]:
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
                    trade_all += 1

            else:
                days_open += 1  # Increment the days the position has been open

                if mspreads[i] >= stop1[i] and mspreads[i - 1] < stop1[i] and hold_state == 1:
                    profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                    return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                    return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                    return_percentage = 0.5*(return_percentage_A + return_percentage_B)
                    all_trades = all_trades + 1
                    if return_percentage > 0:
                        win = win + 1

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
                    hold_state = 0
                    hold = False
                    days_open = 0  # Reset days_open
                    trades.append(current_trade)
                if mspreads[i] <= stop2[i] and mspreads[i - 1] > stop2[i] and hold_state == -1:
                    profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                    return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                    return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                    return_percentage =0.5*(return_percentage_A + return_percentage_B)
                    all_trades = all_trades + 1
                    if return_percentage > 0:
                        win = win + 1

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
                    hold_state = 0
                    hold = False
                    days_open = 0  # Reset days_open
                    trades.append(current_trade)
                if mspreads[i] <= close1[i] and mspreads[i - 1] > close1[i] and hold_state == 1:
                    profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                    return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                    return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                    return_percentage = 0.5*(return_percentage_A + return_percentage_B)
                    all_trades = all_trades + 1
                    if return_percentage > 0:
                        win = win + 1

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
                    hold_state = 0
                    hold = False
                    days_open = 0  # Reset days_open
                    trades.append(current_trade)
                if mspreads[i] >= close2[i] and mspreads[i - 1] < close2[i] and hold_state == -1:
                    profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                    return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                    return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                    return_percentage =0.5*(return_percentage_A + return_percentage_B)
                    all_trades = all_trades + 1
                    if return_percentage > 0:
                        win = win + 1

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

                    current_trade["duration_days"] = days_open
                    hold_state = 0
                    hold = False
                    days_open = 0
                    trades.append(current_trade)

                # if days_open >= 10:  # Check if the position has been open for more than ten days
                #     # Close the position forcibly
                #     profit = 0  # Assume no profit for forced closure
                #     return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                #     return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                #     return_percentage = 0.5*(return_percentage_A + return_percentage_B)
                #     all_trades = all_trades + 1
                #     if return_percentage > 0:
                #         win = win + 1
                #
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
                #     hold_state = 0
                #     hold = False
                #     days_open = 0  # Reset days_open
                #     trades.append(current_trade)

                if days_open >= 14:  # Check if the position has been open for more than ten days
                    # Close the position forcibly
                    if hold_state == 1:
                        profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                        return_percentage_A = ((hold_price_A - price_A[i]) / hold_price_A) * 100.0
                        return_percentage_B = ((price_B[i] - hold_price_B) / hold_price_B) * 100.0
                        return_percentage = 0.5 * (return_percentage_A + return_percentage_B)

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

                        hold_state = 0
                        hold = False
                        days_open = 0  # Reset days_open
                        trades.append(current_trade)

                        time.append(timestamps[i])
                    elif hold_state == -1:
                        profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                        return_percentage_A = ((price_A[i] - hold_price_A) / hold_price_A) * 100.0
                        return_percentage_B = ((hold_price_B - price_B[i]) / hold_price_B) * 100.0
                        return_percentage = 0.5 * (return_percentage_A + return_percentage_B)

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


                        current_trade["duration_days"] = days_open
                        hold_state = 0
                        hold = False
                        days_open = 0
                        trades.append(current_trade)

                        time.append(timestamps[i])

            profit_list.append(cumulative_return)
            profit_list_A.append(cumulative_return_A)
            profit_list_B.append(cumulative_return_B)

        win_rate = win / all_trades * 100

        print("Total Cumulative Return_A:", cumulative_return_A, "%")
        print("Total Cumulative Return_B:", cumulative_return_B, "%")
        print("Total Cumulative Return:", cumulative_return, "%")
        print("Total Win Rate:", win_rate, "%")
        print("Total Trade Number", trade_all)

        # 记录每个文件的结果
        file_names.append(filename)
        cumulative_returns_A.append(cumulative_return_A)
        cumulative_returns_B.append(cumulative_return_B)
        cumulative_returns.append(cumulative_return)
        win_rates.append(win_rate)
        total_trade_numbers.append(trade_all)

        total_cumulative_return = total_cumulative_return + cumulative_return

# 创建一个包含你的结果的DataFrame
results_df = pd.DataFrame({
    "File Name": file_names,
    "Total Cumulative Return_A (%)": cumulative_returns_A,
    "Total Cumulative Return_B (%)": cumulative_returns_B,
    "Total Cumulative Return (%)": cumulative_returns,
    "Total Win Rate (%)": win_rates,
    "Total Trade Number": total_trade_numbers
})

# 指定要保存的Excel文件名
output_excel_file = "trading_results.xlsx"

# 将DataFrame写入Excel文件
results_df.to_excel(output_excel_file, index=False)

print(f"Results saved to {output_excel_file}")
