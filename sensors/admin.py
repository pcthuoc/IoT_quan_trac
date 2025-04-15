from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from sensors.models import Sensors, SensorData

# -----------------------------
# Resource cho model Sensors
# -----------------------------
class SensorsResource(resources.ModelResource):
    class Meta:
        model = Sensors
        fields = (
            'id', 'sensor_id', 'sensor_name', 'value',
            'unit', 'updated_at'  # Bỏ 'user__username'
        )
        export_order = (
            'id', 'sensor_id', 'sensor_name', 'value',
            'unit', 'updated_at'  # Bỏ 'user__username'
        )

class SensorsAdmin(ImportExportModelAdmin):
    resource_class = SensorsResource
    list_display = ('sensor_id', 'sensor_name', 'value', 'unit', 'updated_at')  # Bỏ 'user'
    list_filter = ('sensor_name',)  # Bỏ 'user'
    search_fields = ('sensor_id', 'sensor_name')
    ordering = ('-updated_at',)

# -----------------------------
# Resource cho model SensorData
# -----------------------------
class SensorDataResource(resources.ModelResource):
    sensor__sensor_id = fields.Field(
        column_name='sensor__sensor_id',
        attribute='sensor',
        widget=ForeignKeyWidget(Sensors, 'sensor_id')
    )

    class Meta:
        model = SensorData
        bulk = False
        fields = (
            'id', 'sensor__sensor_id', 'value', 'unit', 'timestamp'
        )
        export_order = (
            'id', 'sensor__sensor_id', 'value', 'unit', 'timestamp'
        )

class SensorDataAdmin(ImportExportModelAdmin):
    resource_class = SensorDataResource
    list_display = ('sensor', 'value', 'unit', 'timestamp')
    list_filter = ('sensor__sensor_name', 'timestamp')
    search_fields = ('sensor__sensor_id', 'sensor__sensor_name')
    ordering = ('-timestamp',)

# -----------------------------
# Đăng ký các model với admin
# -----------------------------
admin.site.register(Sensors, SensorsAdmin)
admin.site.register(SensorData, SensorDataAdmin)
