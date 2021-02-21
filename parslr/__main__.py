import sys
import os
import timeit
import glob
from junit_xml import TestSuite, TestCase
from parslr.Parslr import Parslr
from parslr.parslr_args import prepare_parser

args = prepare_parser().parse_args()
p = Parslr(args.antlr, args.tmp_path)
ret_val = p.generate_parser(args.grammar)
if ret_val != 0:
    print("Failed to generate parser")
    sys.exit(ret_val)
ret_val = p.compile()
if ret_val != 0:
    print("Failed to compile parser")
    sys.exit(ret_val)

grammar = os.path.splitext(os.path.basename(args.grammar))[0]
if os.path.isdir(args.input):
	# A directory with cases
	test_cases = []
	files = sorted(glob.glob(os.path.join(args.input, "*.txt")))
	failures = 0
	for file in files:
		short = os.path.splitext(os.path.basename(file))[0]
		start = timeit.default_timer()
		result = p.run_test_rig(grammar, args.rule, file)
		end = timeit.default_timer()
		tc = TestCase(short, grammar, end - start, '', '', '')
		if len(result) != 0:
			tc.add_failure_info("fail", str(result))
			failures += 1
		test_cases.append(tc)
	ts = TestSuite(grammar, test_cases)
	if args.output != "":
		with open(args.output, 'w') as f:
			TestSuite.to_file(f, [ts])
	if failures > 0:
		sys.exit(failures)
else:
	# Just one file
	sys.exit(len(p.run_test_rig(grammar, args.rule, args.input)))
