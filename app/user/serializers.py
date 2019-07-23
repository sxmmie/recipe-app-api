from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


# basing this UserSerializer on django framework serializers.ModelSerializer, helps with the
# conversion and creating and retrieving from the database.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # specify the module you want to base your serializer from
        model = get_user_model()    # returns the User model class
        # fields that are going to be converting to/from JSON, when we make HTTP post and
        # we retrieve it in our view and save it into a model.
        # fields to include in the serializer (fields to be made accessible in the API whether to read or write)
        fields = ('email', 'password', 'name')
        # configure extra settings int model.Serializer, to ensure the password at least five characters and read-only
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # this function is callled when we create a new object
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# Endpoint to make a HTTP auth request and generate a temporary auth token,
# that can be used to auth future requests with the API.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for thr user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # whenever you're overwriting the validate function, need to return the attrs
        attrs['user'] = user
        return attrs
