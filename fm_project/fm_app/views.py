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
        trial_no = request.POST.get("trial_no", None)
        trial_service = TrialService(request.POST, trial_no)
        if trial_no:
            trial_service.process_trial_data()
        return JsonResponse(
            trial_service.get_next_trial_data(),
            status=200
        )
