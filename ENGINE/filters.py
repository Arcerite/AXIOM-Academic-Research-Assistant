# ENGINE/filters.py

active_filters = []

def reset_filters():
    active_filters.clear()

def add_filter(filter_str, logic="AND"):
    if not active_filters:
        active_filters.append(filter_str)
        return

    if logic == "AND":
        active_filters.append(filter_str)
    elif logic == "OR":
        active_filters.append(f"|{filter_str}")
    elif logic == "NOT":
        active_filters.append(f"!{filter_str}")

def build_filter_string():
    return ",".join(active_filters)

def get_active_filters():
    return active_filters