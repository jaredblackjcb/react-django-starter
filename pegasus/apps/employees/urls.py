from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views


app_name = 'pegasus_employees'

urlpatterns = [
    path('objects/', TemplateView.as_view(template_name='pegasus/employees/object_lifecycle_home.html',
                                          extra_context={'active_tab': 'object_lifecycle'}),
         name='object_lifecycle_home', ),
    path('objects/django/', views.employee_list, name='django_object_lifecycle'),
    path('objects/django/new/', views.new_employee, name='django_new_employee'),
    path('objects/django/edit/<int:employee_id>/', views.edit_employee, name='django_edit_employee'),
    path('objects/django/delete/<int:employee_id>/', views.delete_employee, name='django_delete_employee'),

    path('objects/htmx/', views.employee_list_htmx, name='htmx_object_lifecycle'),
    path('objects/htmx/new/', views.new_employee_row_htmx, name='htmx_new_employee'),
    path('objects/htmx/empty/', views.empty_htmx, name='htmx_empty'),

    path('objects/htmx/edit/<int:employee_id>/', views.edit_employee_row_htmx, name='htmx_edit_employee'),
    path('objects/htmx/get/<int:employee_id>/', views.get_employee_row_htmx, name='htmx_get_employee'),
    path('objects/htmx/delete/<int:employee_id>/', views.delete_employee_htmx, name='htmx_delete_employee'),

    path('objects/react/', views.ReactObjectLifecycleView.as_view(), name='react_object_lifecycle'),
    path('objects/react/<path:path>', views.ReactObjectLifecycleView.as_view(), name='react_object_lifecycle_w_path'),
    path('charts/', views.ChartsView.as_view(), name='charts'),

    path('api/employee-data/', views.EmployeeDataAPIView.as_view(), name='employee_data'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/employees', views.EmployeeViewSet)

urlpatterns += router.urls
