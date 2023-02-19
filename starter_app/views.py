from allauth.account.views import SignupView
from allauth.account.views import LoginView
from django.urls import reverse


class SubscriptionSignupView(SignupView):

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['price_id'] = self.kwargs['price_id']
        # self.request.session.save()
        return response
    