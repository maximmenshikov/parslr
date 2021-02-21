# Parslr
ANTLR test rig CLI for use in Continuous Integration systems. In short, it generates parser in Java, compiles it, and then tests that no parsing errors occur. At the moment, no validation of output is possible.

## Usage
```python3 -m parslr parameters```

Mandatory parameters are:

 * ```-g <path>``` --- path to grammar.
 * ```-a <path>``` --- path to complete ANTLR jar.
 * ```-r <name>``` --- starting rule.
 * ```-i <path>``` --- path to test input.

The return code is a number of errors during parsing.

## License
MIT
