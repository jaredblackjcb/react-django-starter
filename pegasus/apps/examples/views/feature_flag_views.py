import waffle
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class FeatureFlagExampleView(TemplateView):
    template_name = 'pegasus/examples/example_feature_flag.html'

    def get_context_data(self, **kwargs):
        _create_flag_if_necessary()

        return {
            'active_tab': 'flags',
            'flag_active': waffle.flag_is_active(self.request, 'example-flag')
        }


def _create_flag_if_necessary():
    """Normally this would be done in a Django migration. Doing it here for convenience."""
    waffle.get_waffle_flag_model().objects.get_or_create(
        name='example-flag', defaults={
            "testing": True  # allows enabling via a URL param
        }
    )
