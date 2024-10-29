from datetime import datetime, timedelta

# 定義停車費率參數
WEEKDAY_LIMIT = 130  # 平日每日前16小時上限
WEEKDAY_RATE_FIRST = 16  # 平日前16小時，每30分鐘費率
WEEKDAY_RATE_AFTER = 8   # 平日16小時後，每30分鐘費率

HOLIDAY_LIMIT = 130  # 假日每日上限
HOLIDAY_RATE = 8     # 假日每30分鐘費率

# 假設假日為星期六和星期日，平日為星期一到星期五
def is_weekend(date):
    return date.weekday() >= 5  # 星期六和星期日為假日

# 停車費計算函數
def calculate_parking_fee(entry_time, exit_time):
    total_fee = 0.0
    current_time = entry_time

    while current_time < exit_time:
        # 計算當日結束時間
        day_end = current_time.replace(hour=23, minute=59, second=59)
        end_of_day = min(day_end, exit_time)

        # 計算當日停車時間（以30分鐘為區間，不滿30分鐘算1區間）
        total_minutes = (end_of_day - current_time).total_seconds() / 60
        half_hours = int(total_minutes // 30) + (1 if total_minutes % 30 > 0 else 0)

        # 判斷當日是平日還是假日
        if is_weekend(current_time):
            # 假日計算
            fee = min(half_hours * HOLIDAY_RATE, HOLIDAY_LIMIT)
        else:
            # 平日計算
            if half_hours <= 32:  # 32個半小時區間等於16小時
                fee = min(half_hours * WEEKDAY_RATE_FIRST, WEEKDAY_LIMIT)
            else:
                first_16_hours_fee = WEEKDAY_LIMIT
                additional_hours_fee = (half_hours - 32) * WEEKDAY_RATE_AFTER
                fee = first_16_hours_fee + additional_hours_fee

        # 累加當日停車費
        total_fee += fee
        # 移動到隔天
        current_time = day_end + timedelta(seconds=1)

    return total_fee

# 測試範例
entry_time = datetime.strptime("2024-11-18 03:00", "%Y-%m-%d %H:%M")
exit_time = datetime.strptime("2024-11-18 04:34", "%Y-%m-%d %H:%M")
total_fee = calculate_parking_fee(entry_time, exit_time)
print(f"總停車費用為: {total_fee} 元")
