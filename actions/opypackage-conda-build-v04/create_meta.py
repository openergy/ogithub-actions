import os
import sys

meta = """
package:
  name: __name__
  version: "__version__"

source:
  path: __path__

build:
  number: 0
  script: python -m pip install --no-deps --ignore-installed .
  include_recipe: False
__noarch__

requirements:
  build:
    - python__python_requirement__
    - setuptools 
    - pip
__build_requirements__
  
  run:
    - python__python_requirement__
__dependencies__
"""

if __name__ == "__main__":
    # --- retrieve parameters
    target_dir_path = sys.argv[1]
    repo_name = sys.argv[2]
    arch_specific = sys.argv[3]
    python_requirement = sys.argv[4]

    # --- prepare variables
    version = ""
    path = os.getcwd()
    try:
        with open("./RELEASE.md", "r") as f:
            for line in f.readlines():
                if line.startswith("##"):
                    version = line[2:].strip("#").strip()
                    break
    except:
        raise ValueError("Could not parse version from RELEASE.md")
    if version == "":
        raise ValueError("Could not parse version from RELEASE.md")

    # --- replace meta variables
    if arch_specific == "true":
        meta = meta.replace("__noarch__", "")
        meta = meta.replace("__build_requirements__", "    - cython\n    - numpy")
    else:
        meta = meta.replace("__noarch__", "  noarch: python")
        meta = meta.replace("__build_requirements__", "")
    meta = meta.replace("__name__", repo_name)
    meta = meta.replace("__version__", version)
    meta = meta.replace("__path__", path)
    meta = meta.replace("__python_requirement__", python_requirement)

    # --- manage dependencies
    dependencies = ""
    # try:
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            dependencies += f"    - {line}\n"
    # manage linux requirements
    if arch_specific == "true" and os.path.isfile("./linux_requirements.txt"):
        with open("./linux_requirements.txt", "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                dependencies += f"    - {line}\n"
    meta = meta.replace("__dependencies__", dependencies)

    # write to target
    with open(os.path.join(target_dir_path, "meta.yaml"), "w") as f:
        f.write(meta)
