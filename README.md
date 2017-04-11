# Cluster Pandas

An easy tool to parallelize and distribute your pandas dataframe operation across your cluster or your personal machines.

## Getting Started

### Master

In order to use Cluster Pandas you need a netwrok accessible master running. If you have docker installed in the master machine, just run

`docker run -p 5555:5555 medo/clmaster`

### Slave

Now the master is running, and you can schedule operations. In order to process operations you need at least one slave running. In your slave machine run

`docker run medo/clpandas CL_MASTER_HOST=<YOUR_MASTR_URL>`

### Driver

Now you ready to play with cluster pandas. All you need to do is create a function that takes a dataframe and returns a dataframe.

```python
iris = ...

def area(df):
  df['Sepal.Area'] = df['Sepal.Width'] * df['Sepal.Length']
  return df

```

And now run your function on the iris dataframe

```python
from clpandas.driver import ClusterPandas

cl = ClusterPandas('MASTER_HOST')

job = cl.parallelize(iris, area, 8)

```

You can check the progress of the operatiosn

```python
print("Progress = %d%" % cl.progress(job))
```

To get the result of the operation

```python
cl.collect(job)
```
The result we get here is a single dataframe, in fact cluster pandas runs a merge function on partiions to return reduce the paritions to a single result, by default the function is `pd.concat`. You can get the raw result of the paritions or pass a different merge function

```python
cl.parallelize(iris, apply = area, merge = None)

```

## Manage Dependenices

### Run inside your own Containe

## Provision slaves with AWS Spot Instances


## Architecture

## Why I built this

## Future Work

- Automatically pass a docker container as a dependency of a function instead of restarting the slaves
