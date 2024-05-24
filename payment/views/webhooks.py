from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payment.use_cases.webhooks import ProcessWebhookUseCase

class TransactionWebhookView(APIView):
    def post(self, request):
        payload = request.data  # Assuming your webhook payload is sent in the request data

        # Create an instance of the ProcessWebhookUseCase
        use_case = ProcessWebhookUseCase()

        # Call the use case to process the webhook payload
        success = use_case.execute(payload)

        if success:
            # Respond with a success message and HTTP 200 status code
            return Response({'message': 'Webhook processed successfully'}, status=status.HTTP_200_OK)
        else:
            # Respond with an error message and HTTP 400 status code
            return Response({'message': 'Webhook processing failed'}, status=status.HTTP_400_BAD_REQUEST)
