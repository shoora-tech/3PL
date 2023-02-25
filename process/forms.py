# from django import forms
# from .models import Nomination
# from . import errors

# class NominationActionForm(forms.Form):

#     def form_action(self, nomination):
#         raise NotImplementedError()

#     def save(self, nomination):
#         try:
#             nomination, action = self.form_action(nomination)
#         except errors.Error as e:
#             error_message = str(e)
#             self.add_error(None, error_message)
#             raise

#         return nomination


# class VerifyNominationForm(NominationActionForm):
#     def form_action(self, nomination):
#         nomination.nomination_status = Nomination.APPROVAL_PENDING
#         nomination.save()
#         return nomination
