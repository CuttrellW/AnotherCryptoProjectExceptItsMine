class Scaler():
    def __init__(self, dataset: list, lower_bound=0, upper_bound=1) -> None:
        self.dataset = dataset
        self.min = min(dataset)
        self.max = max(dataset)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def min_max_scale(self):
        scaled_set = []
        try:
            for figure in self.dataset:
                scaled = (figure - self.min) / (self.max - self.min) * (self.upper_bound - self.lower_bound) + self.lower_bound
                scaled_set.append(scaled)
        except ZeroDivisionError:
            print("Error: zero range in captured values. Could not scale dataset.")
        
        return scaled_set
