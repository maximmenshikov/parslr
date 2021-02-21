import sys
import os
from parslr.Parslr import Parslr
from parslr.parslr_args import prepare_parser

args = prepare_parser().parse_args()
p = Parslr(args.antlr, args.tmp_path)
p.generate_parser(args.grammar)
p.compile()
sys.exit(p.run_test_rig(os.path.splitext(os.path.basename(args.grammar))[0],
                        args.rule,
                        args.input))
