from django.db import models


class Contact(models.Model):
    user_from = models.ForeignKey(
        "account.Profile",
        related_name="rel_from_set",
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        "account.Profile",
        related_name="rel_to_set",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["-created"])
        ]
        ordering = ["-created"]
    
    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"