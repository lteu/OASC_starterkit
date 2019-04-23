# counts number of training instances
# License: BSD

import logging
logging.basicConfig(level="INFO")
import json
import time as tm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from aslib_scenario.aslib_scenario import ASlibScenario
from validate import Validator

if __name__ == "__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--train", help="Directory with *all* train data in ASlib format")
    
    args_ = parser.parse_args()
    
    start_time_fold = tm.time()
    train_scenario = ASlibScenario()
    train_scenario.read_scenario(dn=args_.train)
    print ('num of training insts ', len(train_scenario.instances))