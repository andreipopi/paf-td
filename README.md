
## paf-td

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Link to paper](https://proceedings.kr.org/2024/55/)

# Citation

Popescu, A., & Wallner, J. P. (2024). Advancing Algorithmic Approaches to Probabilistic Argumentation under the Constellation Approach. In P. Marquis, M. Ortiz, & M. Pagnucco (Eds.), Proceedings KR (pp. 585-596) https://doi.org/10.24963/kr.2024/55

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

## Instance Format

[RunningExample]
    
    arg(a). arg(b). arg(c). arg(d). arg(e).

    p(a,0.8). p(b,1). p(c,0.9). p(d,1). p(e,1).

    att(a,d). att(d,a). att(b,c). att(c,b). att(a,b). att(b,a). att(c,d).att(d,c). att(e,d). att(d,e).

    p(1,a,d,1). p(2,d,a,1). p(3,a,b,0.7). p(4,b,a,1). p(5,b,c,1). p(6,c,b,1). p(7,d,c,1). p(8,c,d,1). p(9,e,d,0.3). p(10,d,e,0.5).
    
    extension(a).
    extension(c).
    extension(e).

## Authors

Andrei Popescu (TU Graz) and Johannes Wallner (TU Graz). For questions or comments contact andrei.popescu@ist.tugraz.at.

## License

This software is released under the MIT License and copyrighted by the authors.