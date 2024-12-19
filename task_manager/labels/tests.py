from task_manager.labels.models import Label
from task_manager.base import BaseCRUDTest


class LabelCRUDTest(BaseCRUDTest):
    model = Label
    base_url_name = "labels"
    valid_data = {"name": "Bug"}
