from rest_framework import serializers
from django.contrib.auth import get_user_model

class AccountsUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "confirm_password"]

    queryset = get_user_model().objects.all()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        user_instance = self.queryset.create(email = validated_data["email"])
        user_instance.set_password(validated_data["password"])
        user_instance.save()
        return validated_data
