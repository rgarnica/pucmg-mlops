import pandas as pd
import argparse
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import InRangeValidation, InListValidation

parser = argparse.ArgumentParser()
parser.add_argument("inputPath", help="arquivo input Iris", type=str)
parser.add_argument("outputClean", help="arquivo output Iris sem erros", type=str)
parser.add_argument("outputErrors", help="arquivo output Iris com erros", type=str)
args = parser.parse_args()

data = pd.read_csv(args.inputPath)

schema = pandas_schema.Schema([
    Column('sepal_length', [InRangeValidation(4.3, 7.91)]),
    Column('sepal_width', [InRangeValidation(2.0, 4.41)]),
    Column('petal_length', [InRangeValidation(1.0, 6.91)]),
    Column('petal_width', [InRangeValidation(0.1, 2.51)]),
    Column('class', [InListValidation(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])]),
    Column('classEncoder', [InListValidation([0, 1, 2])])
])

errors = schema.validate(data)
errors_index_rows = [e.row for e in errors]
data_clean = data.drop(index=errors_index_rows)
data_clean.drop('class', inplace=True, axis=1)

pd.DataFrame({'col':errors}).to_csv(args.outputErrors)
data_clean.to_csv(path_or_buf=args.outputClean, index=False)




