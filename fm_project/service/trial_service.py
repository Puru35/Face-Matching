"""
This file conatains the processing part of the trial
"""
import os
import json
from pathlib import Path
import random

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
        self.total_score = 0
        self.next_trial_no = self.next_trial_number()

    def next_trial_number(self):
        """
        This method creates the next trial number based on the current trial
        """
        if not self.trial_no:
            return "T1"
        return f"T{int(self.trial_no[1:]) + 1}"

    def get_next_trial_data(self):
        """
        This method returns the data for the next trial
        params:
            data: the data of the completed trial -> dict
            trial_no: the trial number of the completed trial -> str
        return:
            next_trial_data: the required info for the next trial -> dict
        """
        if self.trial_no == "T30":
            return {"message": "Test completed"}
        path = Path(
            __file__).parent / f"..{os.sep}..{os.sep}trial_images{os.sep}{self.next_trial_no}"
        image_name_list = os.listdir(path)
        random.shuffle(image_name_list)
        correct_image_name = ""
        for filename in image_name_list:
            if len(filename.split(".")[0]) is 3:
                correct_image_name = filename
                break
        return {
            "correct_image": correct_image_name,
            "images": image_name_list,
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
        if int(self.trial_no[1:]) and int(self.trial_no[1:]) % 10 == 0:
            cumulative_score = self.add_cumulative_score()
            self.save_trial_data(cumulative_score)
        else:
            self.save_trial_data()
        if self.trial_no == "T30":
            self.json_to_csv()

    def save_trial_data(self, cumulative_score=None):
        """
        This method saves the trial data to the respective file of the user
        """
        path = Path(
            __file__).parent / f"..{os.sep}..{os.sep}json_data{os.sep}{self.name}.json"
        json_filename = path
        trial_data = {
            'trial_no': self.trial_no,
            'trial_type': self.trial_type,
            'correct_image': self.correct_image,
            'image_selected': self.image_selected,
            'is_correct': self.is_correct,
            'time_taken': self.time_taken
        }
        if cumulative_score is not None:
            trial_data['cumulative_score'] = cumulative_score
        try:
            with open(json_filename) as f:
                data = f.read()
                if data:
                    data = json.loads(data)
            existing_trial_data = data.get(self.name)
            existing_trial_data.append(trial_data)
            final_data = {
                self.name: existing_trial_data
            }
        except FileNotFoundError as ex:
            final_data = {
                self.name: [trial_data]
            }
        with open(json_filename, "w") as f:
            f.write(json.dumps(final_data))

    def add_cumulative_score(self):
        """
        This method calculates the cumulative scores for the previous 10 trials
        """
        path = Path(
            __file__).parent / f"..{os.sep}..{os.sep}json_data{os.sep}{self.name}.json"
        json_filename = path
        with open(json_filename) as f:
            data = f.read()
            if data:
                data = json.loads(data)[f'{self.name}']

        sum = 0
        for i in range(len(data) - 10, len(data)):
            sum += data[i].get('is_correct')

        return sum

    def json_to_csv(self):
        import pandas as pd
        path = Path(
            __file__).parent / f"..{os.sep}..{os.sep}json_data{os.sep}{self.name}.json"
        json_filename = path
        with open(json_filename) as f:
            data = f.read()
            if data:
                data = json.loads(data)[f'{self.name}']
        for i in data:
            if i.get("cumulative_score"):
                self.total_score += int(i.get("cumulative_score"))
        data.append({"cumulative_score": self.total_score, "time_taken": "Total Score"})

        with open(json_filename, "w") as f:
            f.write(json.dumps(data))

        with open(json_filename) as f:
            data = f.read()

        dataframe = pd.read_json(data)
        path = Path(
            __file__).parent / f"..{os.sep}..{os.sep}trial_results{os.sep}{self.name}.csv"
        dataframe.to_csv(path, index=False)
