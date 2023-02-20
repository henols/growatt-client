from growatt_client import GrowattClient

# Define the file path and random text to replace the comments
file_path = 'README.md'


def gen_markup():
    client = GrowattClient()

    text = "\n\n| Attribute | Register | Unit | Description | Misc |\n"
    text += "| --- | ---: | --- | --- | --- |\n"

    attributes = client.get_attributes()
    attributes.sort(key=lambda x: x["name"])
    for attr in attributes:
        name = attr["name"]
        d = attr["description"]
        u = attr["unit"]
        calculated = True if "template" in attr else False
        m = ""
        if calculated:
            r = "Calc"
            m = attr["template"]
        else:
            r = attr["pos"]
        text += (f"| {name} | {r} | {u} | {d} | {m} |\n")
    
    return text + '\n'

# Open the file and read its contents
with open(file_path, 'r') as file:
    content = file.read()

# Find the start and end indices of the HTML comments
start_index = content.find('<!-- attr-start -->')
end_index = content.find('<!-- attr-end -->')

new_text = gen_markup()

# Replace the content between the comments with the random text
if start_index != -1 and end_index != -1:
    start_index += len('<!-- attr-start -->')
    content = content[:start_index] + new_text + content[end_index:]

# Save the updated content back to the file
with open(file_path, 'w') as file:
    file.write(content)