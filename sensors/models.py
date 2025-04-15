from django.db import models
from django.utils import timezone

class Sensors(models.Model):
    # Bỏ liên kết user
    updated_at = models.DateTimeField(default=timezone.now)  # Thời gian cập nhật
    sensor_id = models.CharField(max_length=255, unique=True)  # Định danh cảm biến
    sensor_name = models.CharField(max_length=255)  # Tên cảm biến
    value = models.FloatField(null=True, blank=True)  # Giá trị cảm biến
    unit = models.CharField(max_length=50, null=True, blank=True)  # Đơn vị

    def save(self, *args, **kwargs):
        if self.pk is None:
            existing_sensor = Sensors.objects.filter(sensor_id=self.sensor_id).first()
            if existing_sensor:
                self.pk = existing_sensor.pk
                self.updated_at = timezone.now()
        super(Sensors, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.sensor_name} ({self.sensor_id}) - {self.value} {self.unit} at {self.updated_at}"

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE, related_name='data_logs', verbose_name="Cảm biến")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Thời gian ghi nhận")
    value = models.FloatField(verbose_name="Giá trị")
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name="Đơn vị")

    def __str__(self):
        return f"{self.sensor.sensor_name} - {self.value} {self.unit} @ {self.timestamp}"

    class Meta:
        verbose_name = "Dữ liệu cảm biến"
        verbose_name_plural = "Lịch sử cảm biến"
        ordering = ['-timestamp']
