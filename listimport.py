from pathlib import Path
import os

for path in Path('.').rglob('*.py'):
    print(path.name)
    with open(path.absolute()) as f:
        lines = f.readlines()
        for x in lines:
            if "import" in x:
                print(x)
