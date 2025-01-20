from rest_framework.generics import ListAPIView

from banner.models import Banner
from banner.serializers import BannerSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
