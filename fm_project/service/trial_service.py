"""
This file conatains the processing part of the trial
"""
import os


class TrialService:
    """
    In this class, we will process the data of the incoming trial,
    and return the required information of the next trial
    """
    def __init__(self, data=None, trial_no=None):
        self.data = data
        self.trial_no = trial_no
        self.next_trial_no = self.next_trial_number()

    def next_trial_number(self):
        if not self.trial_no:
            return "T1"
        return f"T{int(self.trial_no[1:])+1}"

    def get_next_trial_data(self):
        """
        This method returns the data for the next trial
        params:
            data: the data of the completed trial -> dict
            trial_no: the trial number of the completed trial -> str
        return:
            next_trial_data: the required info for the next trial -> dict
        """
        image_name_list = os.listdir(f"../../trial_images/{self.next_trial_no}")
        correct_image_name = ""
        for filename in image_name_list:
            if len(filename.split(".")[0]) is 3:
                correct_image_name = filename
                break
        return {
            correct_image_name: image_name_list,
            "trial_no": self.next_trial_no
        }
