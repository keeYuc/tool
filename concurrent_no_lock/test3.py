import json
with open('a.txt') as f:
    s = f.read()
    data = [i.strip('\n').strip(' ') for i in s.split(',')]
    json.dump(data[:1000], open('b.json', 'w'))
    #pd.DataFrame([i.strip('\n').strip(' ') for i in s.split(',')]).to_csv("a.csv")
