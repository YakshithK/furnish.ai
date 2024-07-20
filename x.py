first_dash_pos = input_string.find('-')
second_part_start = input_string.find('-', first_dash_pos + 1)

category = input_string[:second_part_start]
name = input_string[second_part_start:].strip('-').split(',')[0]
