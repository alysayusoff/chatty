from django.http import HttpResponse
from rest_framework import mixins, generics
from .models import *
from .serializers import *

class UserDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserDetailsSerializer

    def get(self, request, *args, **kwargs):
        # get user object
        appuser = AppUser.objects.get(user=request.user)
        # check that the keyword argument pk and user's own id is the same, before returning the api
        # the reason i do this is to make sure that users are only able to see their own data, and no one else's
        if kwargs['pk'] == appuser.id:
            return self.retrieve(request, *args, **kwargs)
        else:
            return HttpResponse(status=404)