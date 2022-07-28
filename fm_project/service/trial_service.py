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
        self.name = data.get("name", "")
        self.data = data
        self.trial_no = trial_no
        self.time_taken = None
        self.image_selected = ""
        self.correct_image = ""
        self.is_correct = 0
        self.trial_type = ""
        self.total_score = ""
        self.next_trial_no = self.next_trial_number()

    def next_trial_number(self):
        """
        This method creates the next trial number based on the current trial
        """
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
            "trial_no": self.next_trial_no,
            "name": self.name
        }

    def get_trial_type(self):
        """
        This method extracts the trial type based on the trial number
        """
        split_trial_number = int(self.trial_no[1:])
        if split_trial_number in range(1, 11):
            self.trial_type = "Unmasked to Unmasked"
        elif split_trial_number in range(11, 21):
            self.trial_type = "Masked to Masked"
        else:
            self.trial_type = "Unmasked to Masked"

    def process_trial_data(self):
        """
        This method process the data for each trial,
        and saves the data in a csv file.
        """
        self.image_selected = self.data.get("image_selected")
        self.time_taken = self.data.get("time_taken")
        image_name, extension = self.image_selected.split(".")
        if len(image_name) is 3:
            self.is_correct = 1
            self.correct_image = self.image_selected
        else:
            self.correct_image = f"{image_name[:-1]}.{extension}"
        self.get_trial_type()
        self.save_trial_data()

    def save_trial_data(self):
        """
        This method saves the trial data to the respective file of the user
        """
