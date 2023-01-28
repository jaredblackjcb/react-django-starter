from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from ..forms import ExampleForm


@method_decorator(login_required, name='dispatch')
class ExamplesHomeView(TemplateView):
    template_name = 'pegasus/examples/examples_home.html'

    def get_context_data(self, **kwargs):
        return {
            'active_tab': 'home',
        }


class ExampleFormView(FormView):
    template_name = 'pegasus/examples/example_form.html'
    form_class = ExampleForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        messages.success(self.request, 'Thanks for filling in the form!')
        return HttpResponseRedirect(reverse('pegasus_examples:examples_home'))


# import other views
from .payments_views import *
from .tasks_views import *
from .feature_flag_views import *
