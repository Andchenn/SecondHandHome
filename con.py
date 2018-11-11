import pandas as pd

# Combine two Series.
s1 = pd.Series(['a', 'b'])
s2 = pd.Series(['c', 'd'])
p = pd.concat([s1, s2])
print(p)

# Clear the existing index and reset it in the result by setting the ignore_index option to True.
print(pd.concat([s1, s2], ignore_index=True))

# Add a hierarchical index at the outermost level of the data with the keys option.
print(pd.concat([s1, s2], keys=['s1', 's2', ]))

# Label the index keys you create with the names option.
print(pd.concat([s1, s2], keys=['s1', 's2'], names=['Series name', 'Row ID']))

# Combine two DataFrame objects with identical columns.
df1 = pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])
print(df1)


df2 = pd.DataFrame([['c', 3], ['d', 4]], columns=['letter', 'number'])
print(df2)

print(pd.concat([df1, df2]))

# Combine DataFrame objects with overlapping columns and return everything. Columns outside the intersection will be
# filled with NaN values.
df3 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']], columns=['letter', 'number', 'animal'])
print(df3)


# Combine DataFrame objects with overlapping columns and return only those that are shared by passing inner to the
# join keyword argument.
print(pd.concat([df1, df3], join="inner"))

# Combine DataFrame objects horizontally along the x axis by passing in axis=1.
df4 = pd.DataFrame([['bird', 'polly'], ['monkey', 'george']], columns=['animal', 'name'])
print(pd.concat([df1, df4], axis=1))

# Prevent the result from including duplicate index values with the verify_integrity option.
df5 = pd.DataFrame([1], index=['a'])
print(df5)

df6 = pd.DataFrame([2], index=['a'])
print(df6)
