from rest_framework import serializers
from .models import Artist, ArtistTransaction

from .models import CourseMasterCertificate

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"

class ArtistPaymentRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1000)
    description = serializers.CharField(required=True, max_length=500)

class ArtistTransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArtistTransaction
        fields = "__all__"


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMasterCertificate
        fields = ['id', 'course', 'state',  'issued_to', 'issued_at']

class CertificateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMasterCertificate
        fields = ['course', 'certificate', 'state', 'issued_to']

    def create(self, validated_data):
        return super().create(validated_data)
class CertificateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMasterCertificate
        fields = ['id', 'course', 'state',  'issued_to', 'issued_at','certificate']