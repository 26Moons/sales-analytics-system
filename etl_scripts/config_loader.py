import yaml
import os

# we need a function that will return the contents of yaml
# if we get the contents as dictionary , its meaningful and useable
def load_config(config_path: str = "config/config.yaml") -> dict:
    # this is our argument (var : datatype = value)

    # the bare minimum thing for this function is -> it should 
    # have this file at this path
    if not os.path.exists(config_path) :
        raise FileNotFoundError(f"Config file is not present {config_path}")
    
    # "with" keyword is used in file accessing
    # "open" is a method , needs path and mode
    # this single line result is stored as f
    # yaml.safe_load takes contents of file and turn them in dict
    with open(config_path,"r") as f:
        config = yaml.safe_load(f)

    return config

# if u want to directly run a file
'''
if __name__ == "__main__":
    config = load_config()
    print(config)
'''