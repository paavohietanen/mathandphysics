def pp_json(input):
    output = ""
    indentation_level = 0
    for char in input:
        if char == "{":
            indentation_level += 1
            output += "\n" + "\t"*indentation_level + "{"
        elif char == "}" and indentation_level > 0:
            indentation_level -= 1
            output += char
        elif char == "\n":
            output += char + "\t" * indentation_level
        else:
            output += char
    return output
