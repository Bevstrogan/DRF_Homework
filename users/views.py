from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.services import create_stripe_product, create_stripe_price, create_srtipe_session
from materials.permissions import IsAuth
from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserSerializerPerm,
)


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password((user.password))
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializerPerm
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = User
    queryset = User.objects.all()
    permission_classes = [IsAuth, IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAuthenticated]

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        payment.product = create_stripe_product(product=payment.paid_course)
        payment.price = create_stripe_price(price=payment.payment_amount, product=payment.product)
        payment.session_id, payment.link, payment.status = create_srtipe_session(session=payment.price)
        payment.save()