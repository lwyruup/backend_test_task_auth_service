from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

class BussinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.code


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="access_rules")
    element = models.ForeignKey(
        BussinessElement, on_delete=models.CASCADE, related_name="role_rules"
    )
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    create_permission = models.BooleanField(default=False)

    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)

    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "element")

    def __str__(self) -> str:
        return f"{self.role.name} -> {self.element.code}"

