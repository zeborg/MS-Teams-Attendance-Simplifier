import csv

def fetch(filename):
    def time(t):
        time = t
        y = t.strip().split(':')
        total = float(y[0])*3600+float(y[1])*60+float(y[2])
        return total/60

    if filename != None:
        with open(filename, encoding='utf-16') as csvf:
            content = csv.reader(csvf)
            members = dict()
            c = False
            last = None
            for row in content:
                if c:
                    if row[1] == 'Joined':
                        if row[0] not in members:
                            members[row[0]] = [row[-1], 0, True]
                        else:
                            members[row[0]][0] = row[-1]
                            members[row[0]][2] = True
                    elif row[1] == 'Left':
                        if row[0] not in members:
                            members[row[0]] = [None, time(row[-1]), True]
                        else:
                            members[row[0]][1] = members[row[0]][1] + time(row[-1])-time(members[row[0]][0])
                            members[row[0]][2] = False
                c = True       
                last = row[-1]

            for key in members:
                if members[key][2]:
                    members[key][1] = members[key][1] + time(last) - time(members[key][0])
            
            res = list()
            
            for i in sorted(members.items(), key=lambda v:v[1][1], reverse=True):
                res.append([i[0],str(round(i[1][1],2))])
                
        csvf.close()

        return res

print(fetch('uploads/teams_attd_test.csv'))