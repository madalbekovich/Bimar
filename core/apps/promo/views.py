from rest_framework.decorators import action
from rest_framework import viewsets
from . import models, serializers
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from rest_framework import generics


class BonusPurchaseViewSet(viewsets.GenericViewSet):
    """Зачисления бонуса"""
    queryset = models.PurchasesHistory.objects.all()
    serializer_class = serializers.BonusPurchaseSerializer

    @action(detail=False, methods=['post'])
    def set_purchases(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                result = serializer.save()

                response_data = {
                    "response": True,
                    "message": "Покупка успешно обработана",
                    "total_bonus": result.get('total_bonus', 0),
                    "user_bonus_balance": result['user'].bonus if result.get('user') else 0
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            # logger.error(f"Ошибка при обработке покупки: {str(e)}")
            return Response(
                {"response": False, "error": "Ошибка при обработке покупки"},
                status=status.HTTP_400_BAD_REQUEST
            )

class BonusWriteOff(generics.GenericAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        bonus_id = self.request.GET.get('bonus_id')
        total = self.request.GET.get('total')

        if bonus_id is not None:
            queryset = self.get_queryset().filter(bonus_id=bonus_id).first()
            if queryset:
                if total is not None and total != '':
                    if queryset.bonus >= float(total):
                        queryset.bonus -= float(total)
                        queryset.save()
                        return Response({"response": True, "message": "Списание успешно выполнено", "bonuses": queryset.bonus})
                    return Response({"response": False, "message": "Не хватает бонусов для списания"})
                return Response({"response": False, "message": "Укажите total"})
            return Response({"response": False, "message": "Пользователь не найден"})
        return Response({"response": False, "message": "Укажите bonus_id"})