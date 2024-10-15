
## paf-td

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Paper with appendix](inlcude link)

# Citation



## Problem

paf-td computes the probability of a set of arguments being a \sigma extension in a PAF.


## Usage

The two main systems are in Experiments/td-python/verification: 

-rational_efficient_join
and
-real_efficient_join


[monolithic-clingo]

    clingo encoding_COM_ver.py problem_instance 0 -q    

[monolithic-python]

    python monolithic_solver_ver.py problem_instance

[td-python]

    python post_order_ver.py problem_instance

    (Note that for this system you will need to compile HTD, and set the path to the binary in input_output.py)

## HTD Compilation





## Problem Instance and Query


## Authors

Andrei Popescu (TU Graz) and Johannes Wallner (TU Graz). For questions or comments contact andrei.popescu@ist.tugraz.at.

## License

This software is released under the MIT License and copyrighted by the authors.