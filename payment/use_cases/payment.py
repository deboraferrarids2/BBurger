from payment.models.transaction import Transaction
from order.models.orders import Order
from django.db import transaction

class CreatePaymentUseCase:
    def execute(self, order):
        if order.status != 'em aberto':
            raise Exception('Payment cannot be created for an order that is not in "em aberto" status.')

        # Create a payment transaction
        try:
            with transaction.atomic():
                # Create a new Transaction object
                payment = Transaction(
                    order=order,
                    status='aguardando',  # You can set the initial status as 'pago' or any desired value
                    external_id='',  # You can set an external ID if needed
                )
                payment.save()
        except Exception as e:
            raise Exception('Failed to create payment transaction: {}'.format(str(e)))

        return payment

class CheckoutOrderUseCase:
    def execute(self, order):
        if order.status == 'em aberto':
            # Call the CreatePaymentUseCase to create a payment transaction
            create_payment_use_case = CreatePaymentUseCase()
            create_payment_use_case.execute(order)

            # Update the order status to 'recebido'
            order.status = 'recebido'
            order.save()
        else:
            raise Exception('Esse pedido não pode ser finalizado.')
