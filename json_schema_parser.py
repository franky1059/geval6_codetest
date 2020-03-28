

import sys, os
import traceback
import json


g_cliargs = None



def get_arg_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--file", dest="file", default="", type=str, help="config file path")

    parser.add_argument("-k", "--keypath", dest="keypath", default="", type=str, help="key path")


    return parser



def get_file_contents(file):
    file_contents = ""

    f = open(file,'r',encoding = 'utf-8')
    file_contents = f.read()

    return file_contents



def get_type_for_key_path(schema: dict, key_path: str) -> str: 
    type_for_key_path = None

    # split keypath
    components = key_path.split('.')

    current_schema_block = None
    if "properties" in schema:
        current_schema_block = schema["properties"]
    else:
        raise Exception("schema is not valid!")

    # search json with key path
    for component in components:
        if component in current_schema_block:
            current_schema_block = current_schema_block[component]
            if "$ref" in current_schema_block:
                ref_components = current_schema_block["$ref"].split('/')
                current_schema_block = schema["definitions"][ref_components[-1]]
            if component == components[-1]:
                type_for_key_path = current_schema_block["type"]
            elif "properties" in current_schema_block:
                current_schema_block = current_schema_block["properties"]


    return type_for_key_path






if __name__ == "__main__":

    g_cliargs, unknown = get_arg_parser().parse_known_args(args=sys.argv[1:])

    # get file contents
    file_contents = get_file_contents(g_cliargs.file)
    schema_contents = json.loads(file_contents)

    # parse file json
    type_for_key_path =  get_type_for_key_path(schema = schema_contents, key_path = g_cliargs.keypath) 
    print(type_for_key_path)








    
