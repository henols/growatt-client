from growatt_client import GrowattClient


def gen_markup():
    client = GrowattClient()

    print("| Attribute | Register | Unit | Calculated | Description | Misc |")
    print("| --- | ---: | --- | --- | --- | --- |")

    attributes = client.get_attributes()
    attributes.sort(key=lambda x: x["name"])
    for attr in attributes:
        name = attr["name"]
        d = attr["description"]
        u = attr["unit"]
        calculated = "(calculated)" if "template" in attr else ""
        if calculated:
            m = attr["template"]
            print(f"| {name} | - | {u} | &check; | {d} | {m} |")
        else:
            r = attr["pos"]
            print(f"| {name} | {r} |{u} | | {d} | |")


if __name__ == "__main__":
    gen_markup()
