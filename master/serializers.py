from rest_framework import serializers
from .models import Artist, ArtistTransaction


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