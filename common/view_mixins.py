# https://medium.com/@hassanraza/what-is-dispatch-used-for-in-django-c29af0653e94#:~:text=The%20dispatch%20method%20takes%20in,middleman%20between%20requests%20and%20responses.
from django.shortcuts import redirect


#  if user is logged in -> go to dashboard, else -> Home
class RedirectToDashboardMixin:
    # ~ LoginRequiredMixin
    def dispatch(self, request, *args, **kwargs):
        # test if user is logged in
        if request.user.is_authenticated:
            return redirect('dashboard')
        # else default template
        return super().dispatch(request, *args, **kwargs)

# What is dispatch used for in django?
# https://medium.com/@hassanraza/what-is-dispatch-used-for-in-django-c29af0653e94
"""
you might use this to block/filter certain kinds of requests or even inject arguments…
def dispatch(self, request, *args, **kwargs):
   # Updates the keyword args to always have 'foo' with the value 'bar' 
    if 'foo' in kwargs:
        # Block requests that attempt to provide their own foo value
        return HttpResponse(status_code=400)
    kwargs.update({'foo': 'bar'}) # inject the foo value
    # now process dispatch as it otherwise normally would
    return super().dispatch(request, *args, **kwargs)
"""