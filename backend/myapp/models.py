from django.db import models
from django.utils import timezone
import secrets
import string
# from django.core.mail import send_mail   # keep import commented if not used


def generate_swift_code(length=8):
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_id_transfert(length=12):
    """Generate random alphanumeric transfer ID (letters + numbers)."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class Payment(models.Model):
    id_transfert = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    swift_code = models.CharField(max_length=32, unique=True, blank=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    banque_name = models.CharField(max_length=200)
    numero_compte = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100, blank=True)

    expediteur_nom = models.CharField(max_length=200)
    expediteur_pays = models.CharField(max_length=100, blank=True)
    motif = models.CharField(max_length=255, blank=True)

    expiration_date = models.DateTimeField(null=True, blank=True)
    echeance_date = models.DateTimeField(null=True, blank=True)

    beneficiaire_nom = models.CharField(max_length=200, blank=True, default="")
    beneficiaire_compte = models.CharField(max_length=100, blank=True, default="")
    beneficiaire_telephone = models.CharField(max_length=50, blank=True, default="")
    beneficiaire_email = models.EmailField(blank=True, default="")

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id_transfert:
            self.id_transfert = generate_id_transfert(12)
        if not self.swift_code:
            self.swift_code = generate_swift_code(10)

        super().save(*args, **kwargs)

        # --- Email sending disabled ---
        # if self.beneficiaire_email:
        #     subject = "Notification de virement - MERKFINANCES"
        #     message = (
        #         "Nous vous informons que votre virement a été exécuté avec succès et reste en attente "
        #         "de l’activation finale.\n\n"
        #         "Nous vous invitons à effectuer le suivi via le lien sécurisé suivant afin de compléter "
        #         "la procédure: https://merkfinances.com/\n\n"
        #         f"Code SWIFT de la transaction : {self.swift_code}\n\n"
        #         "Nous restons à votre disposition pour toute information complémentaire.\n"
        #         "MERKFINANCES"
        #     )
        #     try:
        #         send_mail(
        #             subject,
        #             message,
        #             "no-reply@merkfinances.com",  # change to your sender email
        #             [self.beneficiaire_email],
        #             fail_silently=True,
        #         )
        #     except Exception as e:
        #         print(f"Email sending failed: {e}")
        # --- End of disabled block ---

    def __str__(self):
        return f"{self.username or ''} — {self.id_transfert} — {self.swift_code} — {self.banque_name} — {self.montant}"


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.payment.swift_code} — {self.amount} @ {self.timestamp.isoformat()}"
