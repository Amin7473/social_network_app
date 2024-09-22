from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.utils.generic_utils import is_valid_password
class AccountsUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password", "confirm_password", "role"]

    queryset = get_user_model().objects.all()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        if not is_valid_password(attrs["password"]):
            raise serializers.ValidationError("Please choose a strong password")
        return attrs

    def create(self, validated_data):
        user_instance = self.queryset.create(
            email = validated_data["email"].lower(),
            username = validated_data["username"].title(),
            role = validated_data["role"]
        )
        user_instance.set_password(validated_data["password"])
        user_instance.save()
        return validated_data


class AccountsLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Making email validation case insensitive
        email = attrs.get('email').lower()
        password = attrs.get('password')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email__iexact=email)
        except user_model.DoesNotExist:
            raise serializers.ValidationError('No active account found with the given credentials')

        if user and user.check_password(password):
            attrs['email'] = email
            return super().validate(attrs)
        else:
            raise serializers.ValidationError('No active account found with the given credentials')
