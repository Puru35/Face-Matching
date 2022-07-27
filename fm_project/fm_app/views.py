from django.views import View
from django.http.response import JsonResponse

from service import TrialService


class Trial(View):
    """
    In this class, we will receive the data from the FE, process it,
    and send back the data of the next trial. If it is the first trial (T1),
    then we won't be receiving any data
    """

    def post(self, request):
        data = request.POST
        trial_service = TrialService()
        if not data:
            return JsonResponse(trial_service.get_trial_data(), status=200)
        trial_no = request.POST.get("trial_no")
        return JsonResponse(trial_service.get_trial_data(trial_no), status=200)
