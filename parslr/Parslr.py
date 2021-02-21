import argparse
import os
import subprocess
import re
import sys
import timeit
import glob
from junit_xml import TestSuite, TestCase

"""
Main parslr class
"""


class Parslr:

    CLS_ANTLR_TOOL = "org.antlr.v4.Tool"
    CLS_ANTLR_TEST_RIG = "org.antlr.v4.gui.TestRig"
    ERR_PARSER_NOT_READY = "Internal error: parser is not ready"

    def __init__(self):
        self.antlr_path = ""
        self.tmp_path = ""

    def __init__(self, antlr_path, tmp_path):
        self.antlr_path = antlr_path
        self.tmp_path = tmp_path

    def validate(self):
        return os.path.isfile(self.antlr_path) and \
            (not os.path.exists(self.tmp_path) or
             os.path.isdir(self.tmp_path))

    """
    Get Java arguments for different PARSLR modes
    """

    def java_args(self, compiler, cls):
        args = []
        if compiler:
            args += ["javac", "-d", self.tmp_path]
        else:
            args += ["java"]
        args += ["-cp", self.antlr_path]
        if not compiler:
            args += [cls]
        return args

    """
    Generate parser in Java language
    """

    def generate_parser(self, grammar):
        if not self.validate():
            return -1

        antlr_args = ["-no-listener", "-Xexact-output-dir", "-o",
                      self.tmp_path, grammar]
        all_args = self.java_args(
            False, Parslr.CLS_ANTLR_TOOL) + antlr_args
        process = subprocess.Popen(all_args)
        return process.wait()

    def compile(self):
        if not self.validate():
            return -1
        files = [os.path.join(self.tmp_path, f) for f in os.listdir(
            self.tmp_path) if re.match(r'.*\.java', f)]
        all_args = self.java_args(True, "") + files

        process = subprocess.Popen(all_args)
        return process.wait()

    def run_test_rig(self, cls, rule, input):
        if not self.validate():
            return [Parslr.ERR_PARSER_NOT_READY]

        all_args = ["java",
                    "-cp",
                    self.antlr_path + ":" + self.tmp_path,
                    Parslr.CLS_ANTLR_TEST_RIG,
                    cls,
                    rule,
                    input]
        process = subprocess.Popen(all_args,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        errors = []
        while True:
            line = process.stderr.readline()
            if line and line.strip() != "":
                print(line)
                if re.match(".*line.*", line):
                    errors += [line]
            elif process.poll() is not None:
                break

        return errors

    def run_test_rig_on_dir(self, cls, rule, input_dir, output_xml):
        if not self.validate():
            return [Parslr.ERR_PARSER_NOT_READY]
        files = sorted(glob.glob(os.path.join(input_dir, "*.txt")))
        failures = 0
        test_cases = []
        for file in files:
            short = os.path.splitext(os.path.basename(file))[0]
            start = timeit.default_timer()
            result = self.run_test_rig(cls, rule, file)
            end = timeit.default_timer()
            tc = TestCase(short, cls, end - start, '', '', '')
            if len(result) != 0:
                tc.add_failure_info("fail", str(result))
                failures += 1
            test_cases.append(tc)
        ts = TestSuite(cls, test_cases)
        if output_xml != "":
            with open(output_xml, 'w') as f:
                TestSuite.to_file(f, [ts])
        return failures
