import sys
import os
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
sys.exit(len(p.run_test_rig(os.path.splitext(os.path.basename(args.grammar))[0],
                            args.rule,
                            args.input)))
