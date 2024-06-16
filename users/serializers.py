from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"], password=validated_data["password"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializerPerm(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "city", "email"]
