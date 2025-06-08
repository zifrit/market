from django.db import models


class VerificationCode(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = [
            "created_at",
        ]
        db_table = "verification_code"
        verbose_name = "VerificationCode"
        verbose_name_plural = "VerificationCodes"

    def __str__(self):
        return f"{self.user_id}-{self.code}"
