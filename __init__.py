"""Streamlined reader of .INI config files, based on built-in *configparser*
"""

import re
import warnings
import configparser

def read(fIni):
    """Reads an *.INI file object and returns a two-level dict of
       section: key: value collections.
    """
    parser = configparser.ConfigParser()
    parser.read_file(fIni)
    config = {}
    for section in parser.sections():
        fields = parser[section]
        config[section] = {}
        for k, v in fields.items():
            if re.match(r"^\d+$", v):
                config[section][k] = int(v)
            elif re.match(r"^\".+\"$", v):
                config[section][k] = v[1:-1]
            elif re.match(r"^(true|false)$", v.lower()):
                config[section][k] = v.lower() == "true"
            else:
                warnings.warn("Unparsable value for key '%s', skipping" % k)
    return config

def update(config1, config2):
    """Merges configs 1 and 2 by section, which (unlike dict.update()) ensures
       no fields in overlapping sections are lost. Result is in effect the
       union of settings from both files, with settings from config2 overriding
       those in config1. Does not modify either original config dictionary.
    """
    config3 = config1.copy()
    for section in config2.keys():
        if section in config3:
            config3[section].update(config2[section])
        else:
            config3[section] = config2[section]
    return config3

def toTable(config):
    """Transforms a two-level dictionary of configuration options into a
       list-of-dictionaries, each with the following fields:
       * section
       * field
       * value
    """
    table = []
    for section in config.keys():
        for k, v in config[section].items():
            table.append({
                "section": section,
                "field": k,
                "value": v
            })
    return table
