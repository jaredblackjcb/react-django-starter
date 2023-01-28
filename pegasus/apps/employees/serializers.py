from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    department = serializers.ChoiceField(choices=Employee.DEPARTMENT_CHOICES)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'name', 'department', 'salary', 'created_at', 'updated_at')


class AggregateEmployeeDataSerializer(serializers.Serializer):
    # this class exists primarily as a form of documentation for the return type of the EmployeeDataAPIView
    total_costs = serializers.JSONField()
    average_salaries = serializers.JSONField()
    headcounts = serializers.JSONField()
