from django.shortcuts import redirect


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/admin/')
