import json

def get_user_feedback(event):
    print(f"\nFeedback for Event: {event['name']} (Start Time: {event['start_time']}, Length: {event['length']})")
    
    enjoyment = int(input("How much did you enjoy the event? (1-5, where 1 is not enjoyable and 5 is very enjoyable): "))
    exhaustion = int(input("How exhausted do you feel after the event? (1-5, where 1 is not exhausted and 5 is very exhausted): "))
    productivity = int(input("How productive do you think you were during the event? (1-5, where 1 is not productive and 5 is very productive): "))
    
    return enjoyment, exhaustion, productivity

def update_event_scores(event, feedback, count):
    event['enjoyment'] = (event['enjoyment'] * count + feedback[0]) / (count + 1)
    event['exhaustion'] = (event['exhaustion'] * count + feedback[1]) / (count + 1)
    event['productivity'] = (event['productivity'] * count + feedback[2]) / (count + 1)

def main():
    events = [
        {'name': 'Event 1', 'start_time': '10:00 AM', 'length': '1 hour', 'enjoyment': 3, 'exhaustion': 3, 'productivity': 3},
        {'name': 'Event 2', 'start_time': '2:00 PM', 'length': '2 hours', 'enjoyment': 3, 'exhaustion': 3, 'productivity': 3},
        # Add more events as needed
    ]

    feedback_file = 'event_feedback.json'

    try:
        with open(feedback_file, 'r') as file:
            feedback_data = json.load(file)
    except FileNotFoundError:
        feedback_data = {}

    for event in events:
        count = feedback_data.get(event['name'], {}).get('count', 0)
        feedback = get_user_feedback(event)
        update_event_scores(event, feedback, count)
        feedback_data[event['name']] = {'enjoyment': event['enjoyment'], 'exhaustion': event['exhaustion'], 'productivity': event['productivity'], 'count': count + 1}

    with open(feedback_file, 'w') as file:
        json.dump(feedback_data, file, indent=2)

if __name__ == "__main__":
    main()
