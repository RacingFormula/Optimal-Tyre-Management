import numpy as np
import matplotlib.pyplot as plt

class OptimalTyreManagement:
    def __init__(self, config):
        self.compounds = config.get("compounds", [])
        self.race_distance = config.get("race_distance", 50)  # laps
        self.track_temperature = config.get("track_temperature", 30)  # degrees Celsius
        self.pit_stop_time = config.get("pit_stop_time", 20)  # seconds

    def simulate_compound(self, compound):
        wear_rate = compound["wear_rate"]
        base_lap_time = compound["base_lap_time"]
        performance_drop = compound["performance_drop"]

        lap_times = []
        remaining_tyre = 100
        total_time = 0

        for lap in range(1, self.race_distance + 1):
            lap_time = base_lap_time + (100 - remaining_tyre) * performance_drop
            total_time += lap_time

            remaining_tyre -= wear_rate
            remaining_tyre = max(0, remaining_tyre)

            lap_times.append(lap_time)

            if remaining_tyre == 0:  # Force a pit stop
                total_time += self.pit_stop_time
                remaining_tyre = 100

        return {
            "lap_times": lap_times,
            "total_time": total_time
        }

    def optimise_strategy(self):
        results = {}

        for compound in self.compounds:
            name = compound["name"]
            print(f"Simulating strategy for {name} compound...")
            results[name] = self.simulate_compound(compound)

        return results

    def plot_results(self, results):
        laps = range(1, self.race_distance + 1)

        plt.figure(figsize=(14, 8))

        # Plot lap times
        plt.subplot(2, 1, 1)
        for compound, data in results.items():
            plt.plot(laps, data["lap_times"], label=f"{compound} Lap Times")
        plt.title("Lap Times Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Lap Time (s)")
        plt.legend()
        plt.grid(True)

        # Plot total time
        plt.subplot(2, 1, 2)
        total_times = {compound: data["total_time"] for compound, data in results.items()}
        plt.bar(total_times.keys(), total_times.values(), color="skyblue")
        plt.title("Total Race Time Per Compound")
        plt.xlabel("Compound")
        plt.ylabel("Total Time (s)")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    compounds = [
        {
            "name": "Soft",
            "wear_rate": 1.2,
            "base_lap_time": 80,
            "performance_drop": 0.03
        },
        {
            "name": "Medium",
            "wear_rate": 0.9,
            "base_lap_time": 82,
            "performance_drop": 0.02
        },
        {
            "name": "Hard",
            "wear_rate": 0.6,
            "base_lap_time": 85,
            "performance_drop": 0.01
        }
    ]

    config = {
        "compounds": compounds,
        "race_distance": 50,
        "track_temperature": 30,
        "pit_stop_time": 20
    }

    optimiser = OptimalTyreManagement(config)
    results = optimiser.optimise_strategy()
    optimiser.plot_results(results)