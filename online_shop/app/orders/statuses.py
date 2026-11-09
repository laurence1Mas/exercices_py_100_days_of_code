ORDER_STATUS_LABELS = {
    "PROCESSING": "En préparation",
    "SHIPPED": "Expédiée",
    "DELIVERED": "Livrée",
    "CANCELLED": "Annulée",
}

PAYMENT_STATUS_LABELS = {
    "PAID": "Payé (simulation)",
    "REFUNDED": "Remboursé (simulation)",
    "UNPAID": "Non payé",
    "FAILED": "Échec",
}

ORDER_STATUS_TRANSITIONS = {
    "PROCESSING": ("SHIPPED", "CANCELLED"),
    "SHIPPED": ("DELIVERED",),
}
