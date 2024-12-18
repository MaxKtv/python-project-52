from task_manager.mixins import BaseCRUDTest
from task_manager.statuses.models import Status


class StatusCRUDTest(BaseCRUDTest):
    model = Status
    base_url_name = 'statuses'
    valid_data = {'name': 'Новый'}
