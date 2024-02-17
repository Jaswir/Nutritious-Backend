
predictive_template = """
You are a helpful food assistant that takes in photos of foods such as fettucini alfredo, Hamburger, or Chicken tikka Masala. You return to your user a comprehensive list of all of the individual ingredients that are in the food. You should use your reasoning skills to include any ingredient that is most likely in that photo such as a food being cooked with butter etc. Here is an example output: 

ingredient
brioche bun
lettuce
grilled onions
hamburger patty
melted cheese
pickle slices
butter
mayo

This is a picture of the users meal. Given this photo, provide all of the ingredients of this food in csv format. Be careful to include all of the foods that are in the photo, include all individual ingredients you think were used to make the food: 

"""


def generate_template(template, variables):
    """
    Generates a string from a template with placeholders, replacing them with values from a variables dictionary.

    :param template: A string template with placeholders for variables.
                     Placeholders should be in the format {variable_name}.
    :param variables: A dictionary where keys are the names of variables and values are the values to replace in the template.
    :return: A string with placeholders in the template replaced with their corresponding values from the variables dictionary.
    """
    from string import Template

    # Create a Template object with the provided template string
    template = Template(template)

    # Substitute placeholders in the template with the corresponding values from the variables dictionary
    result = template.safe_substitute(variables)

    return result


if __name__ == "__main__":
    # Example usage
    template = predictive_template
    variables = {"name": "John", "place": "the Matrix"}
    result = generate_template(template, variables)
    print(result)
