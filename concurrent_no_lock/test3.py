import json
import pandas as pd
with open('a.txt') as f:
    s = f.read()
    #json.dump([i.strip('\n').strip(' ') for i in s.split(',')], open('b.json', 'w'))
    pd.DataFrame([i.strip('\n').strip(' ') for i in s.split(',')]).to_csv("a.csv")

