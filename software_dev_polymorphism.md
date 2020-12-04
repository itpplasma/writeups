See also: http://ithare.com/infographics-operation-costs-in-cpu-clock-cycles/

We want to build an $n_a \times n_b$ matrix $K$ from two point tuples `xa, xb`
containing point coordinates of dimension $d$. A function `kern` is applied
to each pair of points such that `K[i, j] = kern(xa[i], xb[j])`.

A straightforward implementation that doesn't have to allocate `K` would use

```python
def kern_sqexp(xa, xb):
    return exp(-0.5*sum((xa-xb)**2))

build_K(xa, xb, kern_sqexp, K)
```
with
```python
def build_K(xa, xb, kern, K):
    for i in range(len(xa)):
        for j in range(len(xb)):
            K[i, j] = kern(xa[i], xb[j])
```

In scripting languages like Python this example is very slow due to the loop and
the function call overhead, calling `kern` for $n_a \times n_b$ times. In a
compiled language the function call problem still exists. Usually a compiler
would *inline* a simple routine such as `kern_sqexp`, i.e. just print
its content into the loop instead of calling it. However, if it is passed
at runtime as an *argument* (a function pointer in C) this is impossible to do.

Anyway, on modern CPUs the call overhead should be negligible since AMD
Bulldozer and Intel Sandy Bridge:
https://www.agner.org/optimize/instruction_tables.pdf

Functions like `build_K` are called *higher order functions*, as they have
another function as an argument (see type theory). Some new languages like
Julia or Kotlin treat higher-order functions in a clever way so they can still
inline. For example, in Julia, the final code is compiled just-in-time when
first running a function and can specialize `build_K` to the case with a
specific argument for `kern`.

In C, one can use the preprocessor to automatically generate the specialization
but one loses all type safety.

In other traditional languages, one would use object orientation.
Interestingly, at least for C++, these are still processed at
runtime rather than compile time in a *virtual method table (VMT)*, so
cannot be inlined. There seem to be really interesting workarounds, e.g.
https://dev.to/jeyanthan/compile-time-polymorphism-4bji
At least gfortran10 uses the same technique for Fortran procedure overloading
in classes (suspicion due to "`vtab`" routines generated in object code).

In OO one would define an base type

```python
class MatrixBuilder:
    @abstractmethod
    def kern(xa, xb): return
```

containing an abstract method `kern`. For the actual implementation one then
specializes by inheritance

```python
class SqExpMatrixBuilder(MatrixBuilder):
    def kern(xa, xb): return exp(-0.5*sum((xa-xb)**2))
```

This becomes hard to manage in case multiple combinations of behaviour,
e.g. a product kernel

```python
def build_K_prod(xa, xb, kern1, kern2, kern3, K)
```

or even with a list of kernel functions `kerns[:]`. There the number
of possibilities becomes too large to write a specialized class for every
combination.

To get real compile-time polymorphism in C++, one would use templates instead.
