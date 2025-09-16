import json


JSON_INDENT = 4


class RaceStats:
    def __init__(self, data_filepath: str):
        self.data_filepath = data_filepath
        self.data = self.load_data()
        self.rankings = self.rank()
        self.last_id = max([int(i) for i in self.data.keys()]) if self.data else 0

    def load_data(self) -> dict:
        try:
            with open(self.data_filepath) as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self) -> None:
        with open(self.data_filepath, "w") as f:
            json.dump(self.data, f, indent=JSON_INDENT)

    def rank(self) -> dict:
        rankings = {}
        for race_id, info in self.data.items():
            for racer, score in zip(info["competitors"], info["scores"]):
                if racer not in rankings:
                    rankings[racer] = {"races": 0, "wins": 0, "scores": []}
                rankings[racer]["races"] += 1
                rankings[racer]["scores"].append(score)
                if score == max(info["scores"]):
                    rankings[racer]["wins"] += 1
        return rankings

    def get_average_score(self, racer: str) -> int:
        if racer not in self.rankings:
            return 0
        return sum(self.rankings[racer]["scores"]) // len(self.rankings[racer]["scores"])

    def get_win_percentage(self, racer: str) -> float:
        if racer not in self.rankings:
            return 0.0
        return self.rankings[racer]["wins"] / self.rankings[racer]["races"] * 100

    def add_race(self, competitors: list[str], scores: list[int]) -> None:
        self.last_id += 1
        self.data[str(self.last_id)] = {"competitors": competitors, "scores": scores}
        for competitor, score in zip(competitors, scores):
            if competitor not in self.rankings:
                self.rankings[competitor] = {"races": 0, "wins": 0, "scores": []}
                self.rankings[competitor]["races"] += 1
                self.rankings[competitor]["scores"].append(score)
                if score == max(scores):
                    self.rankings[competitor]["wins"] += 1
        self.save_data()
