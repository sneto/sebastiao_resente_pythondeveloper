import begin


def check_overlapping(first_line, second_line):
    """Check if two lines overlap"""

    if first_line is None or second_line is None:
        print("First and second line must not be None")
        return False

    first_line_start = first_line[0]
    first_line_end = first_line[1]
    second_line_start = second_line[0]
    second_line_end = second_line[1]

    if first_line_start <= second_line_start < first_line_end:
        return True

    if second_line_start <= first_line_start < second_line_end:
        return True

    return False


def get_line_integer_list(line):
    if line is None:
        print("Line must not be empty")
        return None

    if type(line) != list:
        print("Line must be two integers list")
        return None

    if len(line) != 2:
        print("Line must have two values coma separated")
        return None

    if line[0] == line[1]:
        print("Line must have two different integer values")
        return None

    return_list = list()

    for value in line:
        try:
            return_list.append(int(value))
        except ValueError:
            print("All values in line must be valid integers")
            return None

    return_list.sort()
    return return_list


def validate_and_convert_input(input_lines):
    """Convert the input lines to integer arrays"""

    if input_lines is None:
        print("Input lines must not be null")
        return None

    if len(input_lines) == 0:
        print("Input lines must not be empty array")
        return None

    validated_lines = []

    for line in input_lines:
        if not line:
            print("Lines must not be empty")
            return None

        validated_line = get_line_integer_list(line.split(','))

        if validated_line is None:
            print("Line %s is not valid" % (line,))
            return None

        validated_lines.append(validated_line)

    return validated_lines


@begin.start(auto_convert=True)
def main(fl: 'First line', sl: 'Second line'):
    """ Check two lines overlapping"""
    converted_input = validate_and_convert_input([fl, sl])

    if not converted_input:
        return 2

    first_line, second_line = converted_input

    overlap = check_overlapping(first_line, second_line)

    if overlap:
        print("Lines overlap")
        return 0
    else:
        print("Lines do not overlap")
        return 1
