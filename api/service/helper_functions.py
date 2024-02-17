import json

def json_list_to_csv(json_list):
    """
    Converts a list of strings (extracted from JSON) into a CSV-formatted string.

    :param json_list: A list of strings.
    :return: A CSV-formatted string where each element of the list is separated by a comma.
    """
    # Ensure all elements are strings and escape commas if necessary
    csv_string = ','.join([str(item).replace(',', '\\,') for item in json_list])
    return csv_string



def extract_json_list(formatted_string):
    """
    Extracts a list from a formatted string that includes JSON content
    surrounded by extra characters or formatting marks.

    :param formatted_string: A string that contains JSON content with additional formatting.
    :return: A Python list extracted from the JSON content within the string.
    """
    try:
        # Find the positions of the opening and closing square brackets
        start_pos = formatted_string.find('[')
        end_pos = formatted_string.rfind(']') + 1  # +1 to include the bracket in the slice

        # Extract the JSON substring using the identified positions
        if start_pos != -1 and end_pos != -1:
            json_substring = formatted_string[start_pos:end_pos]
            # Parse the JSON substring into a Python list
            python_list = json.loads(json_substring)
            return python_list
        else:
            print("Could not find JSON list boundaries.")
            return None
    except json.JSONDecodeError as e:
        # Handle the case where the substring is not valid JSON
        print(f"Error decoding JSON: {e}")
        return None