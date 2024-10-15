
## paf-td

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Paper with appendix](inlcude link)

# Citation

## Problem
paf-td computes the probability of a set of arguments being a \sigma extension in a PAF.


## Usage

The two main systems are in Experiments/td-python/verification rational and real folders.

[td-python]

    python post_order_ver.py problem_instance

    (Note that for this system you will need to compile HTD, and set the path to the binary in input_output.py). 

The other two systems can be used as a camparison:

[monolithic-clingo]
    clingo encoding_COM_ver.py problem_instance 0 -q    
[monolithic-python]
    python monolithic_solver_ver.py problem_instance

## HTD Compilation

See dedicated folder.

## Authors

Andrei Popescu (TU Graz) and Johannes Wallner (TU Graz). For questions or comments contact andrei.popescu@ist.tugraz.at.

## License

This software is released under the MIT License and copyrighted by the authors.