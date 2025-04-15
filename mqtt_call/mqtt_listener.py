import paho.mqtt.client as mqtt
import threading
import queue
import json
from django.utils import timezone
from sensors.models import Sensors,SensorData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings  # ✅ import settings Django

# Hàng đợi xử lý tin nhắn MQTT
mqtt_message_queue = queue.Queue()

# Callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully.")
        client.subscribe(settings.MQTT_TOPIC)
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# Callback khi nhận được tin nhắn MQTT
def on_message(client, userdata, msg):
    try:
        mqtt_message_queue.put(msg)
        print(f"[MQTT] Message received from topic: {msg.topic}")
    except Exception as e:
        print(f"[ERROR] Failed to enqueue MQTT message: {e}")

def process_mqtt_queue():
    while True:
        try:
            msg = mqtt_message_queue.get()
            topic_parts = msg.topic.split('/')

            if len(topic_parts) == 2 and topic_parts[0] == "IOT":
                sensor_id = topic_parts[1]
                payload = msg.payload.decode("utf-8")

                # Giải mã payload
                try:
                    data = json.loads(payload)
                    value = float(data.get("value"))
                    unit = data.get("unit", "")
                except Exception:
                    value = float(payload)
                    unit = ""

                # Kiểm tra nếu sensor_id đã tồn tại trong cơ sở dữ liệu
                sensor = Sensors.objects.filter(sensor_id=sensor_id).first()

                if sensor:
                    # Kiểm tra nếu thời gian cập nhật đã hơn 5 giây
                    time_difference = timezone.now() - sensor.updated_at
                    if time_difference.total_seconds() > settings.TIME_SAVE*60:  # Nếu hơn 5 giây
                        # Lưu dữ liệu cảm biến vào bảng SensorData
                        SensorData.objects.create(
                            sensor_data=sensor,
                            value=value,
                            timestamp=timezone.now()  # Lưu thời gian hiện tại
                        )

                    # Cập nhật giá trị cảm biến và thời gian cập nhật
                    sensor.value = value
                    sensor.updated_at = timezone.now()
                    sensor.save()

                    # Gửi thông báo WebSocket
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",  # Sửa nhóm thành "sensor_data"
                        {
                            "type": "send_sensor_data",  # Sử dụng cùng loại sự kiện như trong consumer
                            "sensor_id": sensor_id,
                            "value": value,
                            "updated_at": timezone.now().isoformat()  # Thêm thời gian cập nhật vào thông báo nếu cần
                        }
                    )

                else:
                    # Nếu cảm biến không tồn tại, chỉ in ra cảnh báo và bỏ qua
                    print(f"[INFO] Sensor '{sensor_id}' not found, skipping update.")

            else:
                print(f"[WARNING] Invalid topic structure: {msg.topic}")

            mqtt_message_queue.task_done()
        except Exception as e:
            print(f"[ERROR] Error processing MQTT message: {e}")

# Khởi động client MQTT và thread hàng đợi
def start_mqtt_listener():
    client = mqtt.Client()
    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        client.loop_start()

        # Khởi động thread xử lý hàng đợi
        processing_thread = threading.Thread(target=process_mqtt_queue)
        processing_thread.daemon = True
        processing_thread.start()

        print("[MQTT] Listener and queue processor started.")
    except Exception as e:
        print(f"[ERROR] Failed to start MQTT client: {e}")