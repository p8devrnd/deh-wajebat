import datetime
from django import template


register = template.Library()

@register.filter(name='format_time_12hr')
def format_time_12hr(value):
    try:
        # Parse the input time string assuming it's in 24-hour format
        input_time = datetime.datetime.strptime(value, '%H:%M:%S').time()
        # Format the time in 12-hour format with AM/PM
        formatted_time = input_time.strftime('%I:%M %p')
        return formatted_time
    except Exception as e:
        print(e)
        return value

