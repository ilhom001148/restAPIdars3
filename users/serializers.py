from rest_framework import serializers,status
from .models import CustomUser
from rest_framework.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    conf_password=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','phone_number','address','password','conf_password']

    def validate(self,data):
        password=data.get('password',None)
        conf_password=data.get('conf_password',None)

        if password is None or conf_password is None or password != conf_password:
            response={
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'Parollar mos emas yoki xato kiritildi'
            }
            raise ValidationError(response)
        if len([i for i in password if i==' '])>0:
            response={
                'status':status.HTTP_400_BAD_REQUEST,
                'message':'Parollar xato kiritildi'
            }
            raise ValidationError(response)
        return data


    def validate_username(self,username):
        if len(username)<7:
            raise ValidationError({'message':'Username kamida 7 ta bolishi kerak'})
        elif not username.isalnum():
            raise ValidationError({'message':'Usernameda ortiqcha belgilar bolmasligi kerak'})
        elif username[0].isdigit():
            raise ValidationError({'message':'Username raqam bilan boshlanmasin'})
        return username

    def create(self,validated_data):
        validated_data.pop('conf_password')

        user=CustomUser.objects.create_user(**validated_data)
        return user



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','phone_number','address','password']

    def update(self,instance,validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.email=validated_data.get('email',instance.email)
        instance.phone_number=validated_data.get('phone_number',instance.phone_number)
        instance.address=validated_data.get('address',instance.address)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


