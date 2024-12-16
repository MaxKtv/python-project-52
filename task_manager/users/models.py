from django.contrib.auth.models import User


class CustomUser(User):
    def __str__(self):
        full_name = " ".join(filter(None, [self.first_name, self.last_name]))
        return full_name if full_name else self.username
