from rest_framework.decorators import action
from rest_framework import viewsets
from . import models, serializers
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User, BonusCard
from rest_framework import generics


class BonusPurchaseViewSet(viewsets.GenericViewSet):
    """Зачисления бонуса"""
    queryset = models.PurchasesHistory.objects.all()
    serializer_class = serializers.BonusPurchaseSerializer

    @action(detail=False, methods=['post'])
    def purchase(self, request):
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
                {"response": False, "error": str(e), "status": "200"},
                status=status.HTTP_400_BAD_REQUEST
            )


class BonusWriteOff(generics.GenericAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        bonus_id = self.request.GET.get('bonus_id')
        total = self.request.GET.get('total')

        if bonus_id is not None:
            try:
                bonus_card = BonusCard.objects.get(bonus_id__bonus_id=bonus_id)
                queryset = bonus_card.user
            except BonusCard.DoesNotExist:
                return Response({"response": False, "message": "Пользователь не найден"})

            if queryset:
                if total is not None and total != '':
                    if queryset.bonus >= float(total):
                        queryset.bonus -= float(total)
                        queryset.save()
                        return Response(
                            {"response": True, "message": "Списание успешно выполнено", "bonuses": queryset.bonus})
                    return Response({"response": False, "message": "Не хватает бонусов для списания"})
                return Response({"response": False, "message": "Укажите total"})
            return Response({"response": False, "message": "Пользователь не найден"})
        return Response({"response": False, "message": "Укажите bonus_id"})

    @action(detail=False, methods=['get'], url_path='current-bonus')
    def current_bonus(self, request):
        bonus_id = self.request.GET.get('bonus_id')

        if bonus_id is not None:
            user = self.get_queryset().filter(bonus_id=bonus_id).first()
            if user:
                return Response({"response": True, "bonuses": user.bonus, "available_bonus": user.bonus * 70 / 100, "birthday": user.birthday, "first_name": user.first_name, "last_name": user.last_name})
            return Response({"response": False, "message": "Пользователь не найден"})
        return Response({"response": False, "message": "Укажите bonus_id"})


class CurrentBonusView(generics.GenericAPIView):
    """Получение текущего баланса бонусов"""
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        bonus_id = self.request.GET.get('bonus_id')

        if not bonus_id:
            return Response({"response": False, "message": "Укажите bonus_id"})

        try:
            bonus_card = BonusCard.objects.get(bonus_id__bonus_id=bonus_id)
            user = bonus_card.user

            if not user:
                return Response({"response": False, "message": "Пользователь не найден"})

            if not user.activated:
                return Response({
                    "response": False,
                    "message": "Счет пользователя заблокирован, причина: \"Аккаунт не активирован\""
                })

            return Response({
                "response": True,
                "bonuses": float(user.bonus) if user.bonus else 0.00
            })

        except BonusCard.DoesNotExist:
            return Response({"response": False, "message": "Пользователь не найден"})
