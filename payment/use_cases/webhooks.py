from payment.models.transaction import Transaction

class ProcessWebhookUseCase:
    def execute(self, payload):
        hook_type = payload.get('type', None)

        if hook_type == 'transaction':
            transaction_id = payload.get('transaction', {}).get('id', None)
            transaction_status = payload.get('transaction', {}).get('status', None)

            if transaction_id and transaction_status:
                try:
                    # Search for the transaction by ID
                    transaction = Transaction.objects.get(id=transaction_id)

                    # Update the transaction status
                    transaction.status = transaction_status
                    transaction.save()

                    return True  # Indicate successful processing
                except Transaction.DoesNotExist:
                    # Handle the case where the transaction does not exist
                    return False
        return False
