from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .services import send_sms
from .serializers import *
from .models import *


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            phone = serializer.data["phone"]
            user = User.objects.get(phone=phone)

            sms = send_sms(phone, "Ваш код подтверждения", user.code)
            if sms:
                return Response(
                    {
                        "response": True,
                        "message": _("Код подверждение был отправлен на ваш номер."),
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"response": False, "message": _("Something went wrong!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors)


class VerifyPhoneView(GenericAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            phone = serializer.data["phone"]

            try:
                user = User.objects.get(phone=phone)

                if user.activated:
                    return Response({"message": _("Аккаунт уже подтвержден")})

                if user.code == code:
                    user.activated = True
                    user.save()

                    token, created = Token.objects.get_or_create(user=user)

                    return Response(
                        {
                            "response": True,
                            "message": _("Пользователь успешно зарегистрирован."),
                            "token": token.key,
                        }
                    )
                return Response(
                    {"response": False, "message": _("Введен неверный код")}
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с таким телефоном не существует"),
                    }
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendCodeView(GenericAPIView):
    serializer_class = SendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            with open('phones.txt', 'w') as log:
                log.write(phone)
            try:
                user = User.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "reponse": False,
                        "message": _("Пользователь с таким телефоном не существует"),
                    },
                )
            if not user.activated:
                user.save()

                sms = send_sms(phone, "Ваш новый код подтверждения", user.code)

                return Response({"response": True, "message": _("Код отправлен")})

            return Response(
                {"response": False, "message": _("Аккаунт уже подтвержден")}
            )
        return Response(serializer.errors)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = request.data.get("phone")
            password = request.data.get("password")

            try:
                get_user = User.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")

            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с указанными телефоном не существует"),
                    }
                )

            user = authenticate(request, phone=f"{''.join(filter(str.isdigit, phone))}", password=password)

            if not user:
                return Response(
                    {
                        "response": False,
                        "message": _("Неверный пароль"),
                    }
                )

            if user.activated:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "response": True,
                        "message": "",
                        "token": token.key,
                    }
                )
            sms = send_sms(phone, "Ваш новый код подтверждения", user.code)
            return Response(
                {
                    "response": False,
                    "message": _("Подвердите номер чтобы войти!"),
                    "isactivated": False,
                },
            )

        return Response(serializer.errors)


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_info = UserInfoSerializer(request.user, context={"request": request}).data
        return Response(user_info)


class UpdatePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            password = serializer.data["password"]
            confirm_password = serializer.data["confirm_password"]

            if password != confirm_password:
                return Response({"response": False, "message": _("Пароли не совпадают")})

            if not user.check_password(old_password):
                return Response({"response": False, "message": _("Вы ввели неправильный старый пароль")})

#            if old_password == password:
#                return Response({"response": False, "message": _("Новый пароль не должен совпадать со старым.")})

            user.set_password(password)
            user.save()

            return Response({"response": True, "message": _("Пароль успешно обновлен")})
        return Response(serializer.errors)


class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
#            old_password = serializer.data["old_password"]
            password = serializer.data["password"]
            confirm_password = serializer.data["confirm_password"]
            if password != confirm_password:
                return Response({"response": False, "message": _("Пароли не совпадают")}, status=status.HTTP_400_BAD_REQUEST)
#            if not user.check_password(old_password):
#                return Response({"response": False, "message": _("Старый пароль неверный")}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()

            return Response({"response": True, "message": _("Пароль успешно обновлен")})
        return Response(serializer.errors)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            try:
                user = User.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")
                user.save()

                send_sms(phone, "Подтвердите номер для сброса пароля", user.code)
                return Response({"response": True, "message": _("Код подверждение был отправлен на ваш номер")})
            except ObjectDoesNotExist:
                return Response({"response": False, "message": _("Пользователь с таким номером не существует")})
        return Response(serializer.errors)


class ResetPasswordVerifyView(GenericAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            phone = serializer.data["phone"]
            with open('phones.txt', 'w') as log:
                log.write(phone)
            try:
                user = User.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")

                if user.code == code:
                    token, created = Token.objects.get_or_create(user=user)

                    return Response({"response": True, "token": token.key})
                return Response({"response": False, "message": _("Введен неверный код")})
            except ObjectDoesNotExist:
                return Response({"response": False, "message": _("Пользователь с таким номером не существует")})
        return Response(serializer.errors)


class UpdateUserDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserDetailSerializer

    def patch(self, request):
        user = request.user

        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"response": True})
        return Response(serializer.errors)


class NotificationView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = NotificationSerializer

    def get(self, request):
        user_info = self.serializer_class(request.user).data
        return Response(user_info)

    def post(self, request):
        user = request.user

        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"response": True})
        return Response(serializer.errors)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'message': 'Вы вышли с аккаунта!', 'response': True}, status=status.HTTP_200_OK)


class SendCodeView(GenericAPIView):
    serializer_class = SendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            with open("phones.txt", 'w') as f:
                f.write(phone)
            try:
                user = User.objects.get(phone=phone)

            except ObjectDoesNotExist:
                return Response(
                    {
                        "reponse": False,
                        "message": _("Пользователь с таким телефоном не существует"),
                    },
                )
            if not user.activated:
                user.save()

                sms = send_sms(phone, "Ваш новый код подтверждения", user.code)

                return Response({"response": True, "message": _("Код отправлен")})

            return Response(
                {"response": False, "message": _("Аккаунт уже подтвержден")}
            )
        return Response(serializer.errors)






class CardScanView(GenericAPIView):
    serializer_class = CardScanSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            barcode_id = serializer.validated_data['barcode_id']

            try:
                bonus_id = BonusId.objects.get(bonus_id=barcode_id)
                bonus_card = BonusCard.objects.get(bonus_id=bonus_id)

                if bonus_card.user:
                    return Response({
                        "message": "Успешно теперь введите пароль от карты",
                        "response": True,
                        "status": "password_required"
                    })
                else:
                    return Response({
                        "message": "Введите ваши данные для регистрации",
                        "response": True,
                        "status": "registration_required"
                    })

            except (BonusId.DoesNotExist, BonusCard.DoesNotExist):
                user_data_1c = self.check_user_in_1c(barcode_id)

                if user_data_1c:
                    user = self.create_user_from_1c(user_data_1c, barcode_id)
                    return Response({
                        "message": "Вы есть в базе 1С, установите пароль на вашу карту",
                        "response": True,
                        "status": "set_password",
                        "user_data": {
                            "name": user_data_1c.get('name'),
                            "phone": user_data_1c.get('phone')
                        }
                    })
                else:
                    return Response({
                        "message": "Карта не найдена",
                        "response": False
                    })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_user_in_1c(self, barcode_id):
        # TODO: Реализовать интеграцию с 1С
        # Пример возвращаемых данных:
        return {
            'barcode_id': barcode_id,
            'name': 'Иван Иванов',
            'phone': '+996700123456',
            'bonus': 1500.00
        }

    def create_user_from_1c(self, user_data_1c, barcode_id):
        bonus_id, created = BonusId.objects.get_or_create(bonus_id=barcode_id)

        user = User.objects.create(
            username=user_data_1c['name'],
            phone=user_data_1c['phone'],
            bonus=user_data_1c.get('bonus', 0),
            activated=False
        )

        bonus_card, created = BonusCard.objects.get_or_create(
            bonus_id=bonus_id,
            defaults={'user': user}
        )

        if not created:
            bonus_card.user = user
            bonus_card.save()

        user.bonus_id = bonus_card
        user.save()

        return user


class CardPasswordView(GenericAPIView):
    serializer_class = CardPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            barcode_id = serializer.validated_data['barcode_id']
            password = serializer.validated_data['password']

            try:
                bonus_id = BonusId.objects.get(bonus_id=barcode_id)
                bonus_card = BonusCard.objects.get(bonus_id=bonus_id)
                user = bonus_card.user

                if user and user.check_password(password):
                    if user.activated:
                        token, created = Token.objects.get_or_create(user=user)
                        return Response({
                            "message": "Вы успешно зашли в систему",
                            "response": True,
                            "token": token.key
                        })
                    else:
                        return Response({
                            "message": "Аккаунт не активирован",
                            "response": False
                        })
                else:
                    return Response({
                        "message": "Вы неверно ввели пароль",
                        "response": False
                    })

            except (BonusId.DoesNotExist, BonusCard.DoesNotExist):
                return Response({
                    "message": "Карта не найдена",
                    "response": False
                })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardSetPasswordView(GenericAPIView):
    serializer_class = CardSetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            barcode_id = serializer.validated_data['barcode_id']
            password = serializer.validated_data['password']

            try:
                bonus_id = BonusId.objects.get(bonus_id=barcode_id)
                bonus_card = BonusCard.objects.get(bonus_id=bonus_id)
                user = bonus_card.user

                if user:
                    user.set_password(password)
                    user.activated = True
                    user.save()

                    token, created = Token.objects.get_or_create(user=user)

                    return Response({
                        "message": "Пароль установлен, вы успешно зарегистрированы",
                        "response": True,
                        "token": token.key
                    })
                else:
                    return Response({
                        "message": "Пользователь не найден",
                        "response": False
                    })

            except (BonusId.DoesNotExist, BonusCard.DoesNotExist):
                return Response({
                    "message": "Карта не найдена",
                    "response": False
                })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardRegistrationView(GenericAPIView):
    """
    Регистрация для новой карты (когда карта есть в системе, но не привязана)
    """
    serializer_class = CardRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            barcode_id = serializer.validated_data['barcode_id']
            name = serializer.validated_data['name']
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']

            try:
                bonus_id = BonusId.objects.get(bonus_id=barcode_id)
                bonus_card = BonusCard.objects.get(bonus_id=bonus_id)

                if bonus_card.user:
                    return Response({
                        "message": "Карта уже привязана к другому пользователю",
                        "response": False
                    })

                if User.objects.filter(phone=phone).exists():
                    return Response({
                        "message": "Пользователь с таким номером уже существует",
                        "response": False
                    })

                try:
                    user = User(
                        username=name,
                        phone=phone,
                        activated=True,
                        registration_source='card'
                    )
                    user.set_password(password)
                    user.save()

                    bonus_card.user = user
                    bonus_card.save()

                    user.bonus_id = bonus_card
                    user.save(update_fields=['bonus_id'])

                    token, created = Token.objects.get_or_create(user=user)

                    return Response({
                        "message": "Вы успешно зарегистрированы",
                        "response": True,
                        "token": token.key
                    })

                except Exception as e:
                    return Response({
                        "message": f"Ошибка при создании пользователя: {str(e)}",
                        "response": False
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except (BonusId.DoesNotExist, BonusCard.DoesNotExist):
                return Response({
                    "message": "Карта не найдена",
                    "response": False
                })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
