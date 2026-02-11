from django.contrib import admin
from .models import Payment, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    readonly_fields = ('timestamp',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'id_transfert',
        'swift_code',
        'banque_name',
        'montant',
        'expediteur_nom',
        'pays',
        'created_at'
    )
    search_fields = (
        'username',
        'id_transfert',
        'swift_code',
        'banque_name',
        'expediteur_nom',
        'numero_compte'
    )
    readonly_fields = ('id_transfert', 'swift_code', 'created_at')
    inlines = [TransactionInline]

    fieldsets = (
        (None, {
            'fields': (
                ('username', 'id_transfert', 'swift_code'),
                ('montant', 'banque_name', 'numero_compte')
            )
        }),
        ('Location', {
            'fields': (('pays', 'ville'),)
        }),
        ('Expéditeur', {
            'fields': (('expediteur_nom', 'expediteur_pays'),)
        }),
        ('Bénéficiaire', {
            'fields': (
                'beneficiaire_nom',
                'beneficiaire_compte',
                'beneficiaire_telephone',
                'beneficiaire_email'
            )
        }),
        ('Dates', {
            'fields': ('expiration_date', 'echeance_date')
        }),
        ('Details', {
            'fields': ('motif',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'description', 'timestamp')
    search_fields = ('payment__username', 'payment__swift_code', 'description')
