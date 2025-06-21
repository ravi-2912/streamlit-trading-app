import re

# 1. PascalCase → snake_case
def pascal_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

# 2. PascalCase → Title Case
def pascal_to_title(s):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s).title()

# 3. snake_case → PascalCase
def snake_to_pascal(s):
    return ''.join(word.capitalize() for word in s.split('_'))

# 4. snake_case → Title Case
def snake_to_title(s):
    return s.replace('_', ' ').title()

# 5. Title Case → snake_case
def title_to_snake(s):
    return re.sub(r'\s+', '_', s.strip().lower())

# 6. Title Case → PascalCase
def title_to_pascal(s):
    return ''.join(word.capitalize() for word in s.strip().split())

# --- Demo ---
if __name__ == "__main__":
    pascal = "AbcDef"
    snake = "abc_def"
    title = "Abc Def"

    print("Pascal → Snake:", pascal_to_snake(pascal))     # abc_def
    print("Pascal → Title:", pascal_to_title(pascal))     # Abc Def

    print("Snake → Pascal:", snake_to_pascal(snake))      # AbcDef
    print("Snake → Title:", snake_to_title(snake))        # Abc Def

    print("Title → Snake:", title_to_snake(title))        # abc_def
    print("Title → Pascal:", title_to_pascal(title))      # AbcDef
