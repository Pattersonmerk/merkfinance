from rest_framework import serializers
from .models import Payment, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'description',
            'timestamp',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'id_transfert',
            'username',
            'swift_code',
            'montant',
            'banque_name',
            'numero_compte',
            'pays',
            'ville',
            'expediteur_nom',
            'expediteur_pays',
            'motif',
            'expiration_date',
            'echeance_date',
            'beneficiaire_nom',
            'beneficiaire_compte',
            'beneficiaire_telephone',
            'beneficiaire_email',
            'created_at',
            'transactions',
        ]
