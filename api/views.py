from itertools import permutations

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.serializers import ArticlesSerializer
from web.models import Articles


@api_view()
def test_view(request):
    return Response({"status" : "ok"})


@api_view(["GET"])
@permission_classes([])
def articles_view(request):
    articles = Articles.objects.all().select_related("user").prefetch_related("tags")
    serializer = ArticlesSerializer(articles, many=True)
    return Response(serializer.data)
