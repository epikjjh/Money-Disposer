from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class DisposeView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request):
        return Response("Hello")
