inirdr
======

Basic Python module for fast loading of config files in INI format.

Module includes three functions, based on built-in *configparser* module:

* read() returns a two-level config dictionary (organized by section) loaded
  from the given file object

* update() returns the union of two two-level config dictionaries, in which the
  latter overrides the former

* toTable() returns a flat list of dictionaries describing each entry in the
  given two-level config dictionary
