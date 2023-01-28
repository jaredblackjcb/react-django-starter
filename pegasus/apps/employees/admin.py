from django.contrib import admin

from .models import Employee



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'department', 'salary', 'created_at']
    list_filter = ['created_at']
