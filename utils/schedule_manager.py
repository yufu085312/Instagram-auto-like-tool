def load_schedule():
    with open("config/schedule.txt", "r") as file:
        return file.read().strip()
