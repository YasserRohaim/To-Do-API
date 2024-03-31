from . import views
from django.urls import path

urlpatterns=[
    path("sign-up",views.sign_up),
    path("sign-in",views.sign_in),
    path("tasks/create-task",views.create_task),
    path("tasks",views.task_list),
    path("tasks/<int:task_id>",views.task_details),
    path("tasks/update-task/<int:task_id>",views.update_task),
    path("tasks/delete-finished",views.delete_finished),
    path("tasks/clear-tasks",views.clear_tasks),
    path("categories",views.category_list),
    path("categories/create-category",views.create_category),
    path("categories/<int:category_id>",views.category_details),
    path("categories/pdate-category/<int:category_id>",views.update_category)

]