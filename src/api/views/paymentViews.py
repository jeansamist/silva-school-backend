from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PaymentSerializer
from ..models import Payment
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)


class ClassLevelPaymentTypeView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
