import csv
from datetime import datetime, timedelta
import random

def generate_beautiful_value(sensor_type):
    if sensor_type == 'turbidity':
        return round(random.uniform(10.0, 45.0), 1)
    elif sensor_type == 'ph':
        return round(random.uniform(6.5, 8.0), 2)
    elif sensor_type == 'tds':
        return round(random.uniform(50.0, 180.0), 1)
    elif sensor_type == 'temp':
        return round(random.uniform(25.0, 31.0), 1)

def generate_peak_value(sensor_type):
    if sensor_type == 'turbidity':
        return 49.9
    elif sensor_type == 'ph':
        return 8.49
    elif sensor_type == 'tds':
        return 199.9
    elif sensor_type == 'temp':
        return 31.9

def generate_sensor_data():
    sensors = [
        {'id': 'sensor_turbidity', 'name': 'Cảm biến độ đục', 'unit': '%'},
        {'id': 'sensor_ph', 'name': 'Cảm biến PH', 'unit': 'pH'},
        {'id': 'sensor_tds', 'name': 'Cảm biến TDS', 'unit': '%'},
        {'id': 'sensor_temp', 'name': 'Nhiệt Độ', 'unit': '°C'}
    ]

    end_time = datetime(2025, 4, 15, 1, 55, 0)
    start_time = end_time - timedelta(days=7)

    # Tạo danh sách mốc thời gian
    time_points = []
    current_time = start_time
    while current_time <= end_time:
        time_points.append(current_time)
        current_time += timedelta(minutes=5)

    # Tổng số bản ghi
    total_rows = len(time_points) * len(sensors)
    current_id = total_rows  # bắt đầu từ ID lớn nhất

    # Chọn thời điểm đỉnh
    peak_times = {
        sensor['id']: random.choice(time_points)
        for sensor in sensors
    }

    with open('beautiful_sensor_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'sensor__sensor_id', 'sensor__sensor_name', 'value', 'unit', 'timestamp'])

        for timestamp in time_points:
            for sensor in sensors:
                sensor_type = sensor['id'].split('_')[1]

                if timestamp == peak_times[sensor['id']]:
                    value = generate_peak_value(sensor_type)
                else:
                    value = generate_beautiful_value(sensor_type)

                writer.writerow([
                    current_id,
                    sensor['id'],
                    sensor['name'],
                    value,
                    sensor['unit'],
                    timestamp.strftime('%Y-%m-%d %H:%M:%S')
                ])
                current_id -= 1  # giảm dần

    print("✅ Đã tạo xong file beautiful_sensor_data.csv với ID giảm dần!")

if __name__ == '__main__':
    generate_sensor_data()
