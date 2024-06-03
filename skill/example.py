items = []

def skill_add_item(args):
    # add an item to the list
    items.append(args[0])
    print(f"Added item: {args[0]}")

def skill_list_items(args):
    # Lists all items in the list.
    print("Items in the list:")
    for item in items:
        print(f"- {item}")