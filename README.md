# PAF-TD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> [!NOTE]
> This is the maintained GitHub repository for PAF-TD. The project was originally hosted in the [TU Graz Knowledge Representation and Reasoning (KRR) GitLab repository](https://gitlab.tugraz.at/krr/paf-td).

PAF-TD provides exact algorithms for computing the probability that a given set of arguments is a complete extension of a Probabilistic Argumentation Framework (PAF) under the constellation approach. The main implementation uses dynamic programming over tree decompositions and is designed to exploit low treewidth. Monolithic Python and Answer Set Programming (ASP) implementations are included for comparison.

## Publication

Andrei Popescu and Johannes P. Wallner. **Advancing Algorithmic Approaches to Probabilistic Argumentation under the Constellation Approach.** In *Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning (KR 2024)*, pages 585-596, 2024.

- [Published paper](https://doi.org/10.24963/kr.2024/55)

## Contents

- [`Experiments/td-python/`](Experiments/td-python/): tree-decomposition-based solvers using rational or floating-point arithmetic
- [`Experiments/monolithic-python/`](Experiments/monolithic-python/): monolithic Python implementations
- [`Experiments/monolithic-clingo/`](Experiments/monolithic-clingo/): monolithic ASP implementation
- [`Instances/`](Instances/): small examples and test instances
- [`InstanceGenerator/`](InstanceGenerator/): benchmark generators
- [`PreProcessing/`](PreProcessing/): ASP-based preprocessing
- [`Experiments/`](Experiments/): benchmark instances, run scripts, raw logs, and compiled results
- [`CompilationHTD/`](CompilationHTD/): the modified HTD entry point and compilation notes

## Requirements

- Python 3
- [pandas](https://pandas.pydata.org/) for the tree-decomposition solvers
- [Clingo](https://potassco.org/clingo/) for the ASP implementation and preprocessing
- [HTD](https://github.com/mabseher/htd) for computing tree decompositions

## HTD Setup

Compile HTD using the modified [`main.cpp`](CompilationHTD/main.cpp) and the instructions in [`CompilationHTD/compileHTD.md`](CompilationHTD/compileHTD.md). Prebuilt binaries are included with the experimental code, but they are platform-specific and may need to be rebuilt.

Set the `command` variable in the following files to the path of your HTD binary:

- [`Experiments/td-python/verification/rational/input_output.py`](Experiments/td-python/verification/rational/input_output.py)
- [`Experiments/td-python/verification/real/input_output.py`](Experiments/td-python/verification/real/input_output.py)

Both files currently contain the placeholder `htd_binary_path`.

## Running the Solvers

From the repository root, run the exact tree-decomposition solver with rational arithmetic:

```bash
python3 Experiments/td-python/verification/rational/post_order_ver.py \
  Instances/running_example.lp
```

The floating-point version is available under `Experiments/td-python/verification/real/`.

The monolithic Python implementation does not require HTD:

```bash
python3 Experiments/monolithic-python/verification/rational/monolithic_solver_ver.py \
  Instances/running_example.lp
```

The ASP implementation uses integer-scaled probabilities. Run it with one of the instances in an `*_asp` directory:

```bash
cd Experiments/monolithic-clingo/verification
python3 monolithic_clingo_ver.py \
  ../../instance-set/other_sets/generated_instances_asp/k3_n5_qa9_1.lp
```

The scripts in [`Experiments/Run/`](Experiments/Run/) reproduce the original experiments but contain absolute paths from the original machines. Update those paths before running the benchmark scripts.

## Instance Format

See [`Instances/running_example.lp`](Instances/running_example.lp) for a complete example. The main predicates are:

- `arg(a).`: argument `a`
- `att(a,b).`: attack from `a` to `b`
- `p(a,0.8).`: probability of argument `a`
- `p(i,a,b,0.7).`: probability of attack `i` from `a` to `b`
- `extension(a).`: argument `a` belongs to the set being verified

## Citation

```bibtex
@inproceedings{PopescuWallner2024,
  author    = {Andrei Popescu and Johannes P. Wallner},
  title     = {Advancing Algorithmic Approaches to Probabilistic Argumentation under the Constellation Approach},
  booktitle = {Proceedings of the 21st International Conference on Principles of Knowledge Representation and Reasoning},
  pages     = {585--596},
  year      = {2024},
  doi       = {10.24963/kr.2024/55}
}
```

## Authors

- Andrei Popescu
- Johannes P. Wallner

For questions or comments, contact [Andrei Popescu](mailto:andrei.popescu@tugraz.at).

## License

The project code is available under the [MIT License](LICENSE). Included third-party tools retain their own licenses.
