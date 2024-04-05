import pandas as pd


df = pd.read_csv("titanic.csv")
print(df)

# วิธีการเรียกดูค่าใน column
# df['Surived']
# df.Servived

print(df.info())

age_not_null = df.Age.notnull()
dq_age = age_not_null.sum() / len(age_not_null)
print(dq_age)

cabin_not_null = df.Cabin.notnull()
dq_cabin = cabin_not_null.sum() / len(cabin_not_null)
print(dq_cabin)

embbarked_not_null = df.Embarked.notnull()
dq_embbarked = embbarked_not_null.sum() / len(embbarked_not_null)
print(dq_embbarked)

print(f"Completeness: {(dq_age+dq_cabin+dq_embbarked)/3}")
