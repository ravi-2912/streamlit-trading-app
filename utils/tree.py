import pandas as pd

def resolve_enum_value(enum_class, key_val: str):
    try:
        member_name = key_val.split(".")[-1]
        print(11111, enum_class, member_name, key_val, sep="---")
        return getattr(enum_class, member_name).value
    except (AttributeError, TypeError):
        return key_val


def build_tree(df: pd.DataFrame, group_keys: list, path_parts: list = [], enum_mapping: dict = {}, ungroup_keys: list = []):
    if df.empty:
        return []

    if not group_keys:
        leaves = []
        for _, row in df.reset_index().iterrows():
            label_parts = [row["Name"]]
            for key in ungroup_keys:
                if key in row and pd.notna(row[key]):
                    enum_cls = enum_mapping.get(key)
                    value = resolve_enum_value(enum_cls, str(row[key]))
                    label_parts.append(value)
            label = " ".join(label_parts)

            leaf = {
                "label": label,
                "value": row["ID"],
            }
            leaves.append(leaf)
        return leaves

    current_key = group_keys[0]
    tree = []

    for key_val, group_df in df.groupby(current_key, dropna=False):
        enum_cls = enum_mapping.get(current_key)
        value = resolve_enum_value(enum_cls, str(key_val))
        new_path = path_parts + [value]
        # label = resolve_enum_value(enum_cls, str(key_val))
        node = {
            "label": value,
            "value": "-".join(new_path),
        }
        children = build_tree(group_df, group_keys[1:], new_path, enum_mapping=enum_mapping, ungroup_keys=ungroup_keys)
        if children:
            node["children"] = children
        tree.append(node)

    return tree