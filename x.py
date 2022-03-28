from tkinter import CENTER
import pandas as pd
import numpy as np
import math
import json
content=pd.read_csv("content.csv",index_col=False)
relation=pd.read_csv("relationship.csv")
user=pd.read_csv("user.csv")
test=pd.read_csv("test.csv")
ans={}
relations={}
replace_lan=[content["language"]=='english',content["language"]=='tamil',content["language"]== 'hindi',content["language"]== 'marathi',content["language"]== 'malayalam' ,content["language"]=='punjabi' ,content["language"]=='kannada'
 ,content["language"]=='oriya' ,content["language"]=='telugu' ,content["language"]=='gujarati' ,content["language"]=='bengali']
replace_lan_val=[1,2,3,4,5,6,7,8,9,10,11]
replce_gen=[content["genre"]=='drama',content["genre"]=='comedy',content["genre"]== 'cricket',content["genre"]== 'action' ,content["genre"]== 'horror' ,content["genre"]== 'documentary' ,content["genre"]== 'sci-fi'
 ,content["genre"]== 'football' ,content["genre"]== 'family' ,content["genre"]== 'tennis' ,content["genre"]== 'mystery' ,content["genre"]== 'badminton' ,content["genre"]== 'basketball'
 ,content["genre"]== 'thriller' ,content["genre"]== 'hockey' ,content["genre"]== 'animation' ,content["genre"]== 'biography' ,content["genre"]== 'fantasy' ,content["genre"]== 'adventure' ,content["genre"]== 'crime'
 ,content["genre"]== 'musical' ,content["genre"]== 'sport']
replace_gen_val=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
content["language"]=np.select(replace_lan,replace_lan_val)
content["genre"]=np.select(replce_gen,replace_gen_val)
content["content_type"]=np.where(content["content_type"]=="series",1,0)

replace_gen=[]



relations={}
print(content)

for i in relation.index:
    if(relation["user_id"][i] in relations):
        relations[relation["user_id"][i]].append(relation["content_id"][i])
    else:
       relations[relation["user_id"][i]]=[relation["content_id"][i]]

ans={}



from sklearn.model_selection import train_test_split
contents={}
for i in content.index:
  contents[content["content_id"][i]]=[content["content_type"][i],content["language"][i],content["genre"][i],content["duration"][i],content["rating"][i],content["episode_count"][i],content["season_count"][i]]
print(contents)



from sklearn.neighbors import NearestNeighbors
# content_id=content["content_id"]
# content=content.drop(["release_date","content_id"],axis=1)

neigh = NearestNeighbors(n_neighbors=10)

neigh.fit(content)
# dis,ind=neigh.kneighbors([[0,0,0,0,0,0,0]])
# print(content["genre"][ind[0][0]])
print(content_id)
for i in test.index:

  id=test["user_id"][i]
  if(id in relations):
    value=relations[id]
    print(len(value))
    out=[0,0,0,0,0,0,0]
    c=0
    for j in value:
       
           
            out[0]+=contents[j][0]
            out[1]+=contents[j][1]
            out[2]+=contents[j][2]
            out[3]+=contents[j][3]
            out[4]+=contents[j][4]
            out[5]+=contents[j][5]
            out[6]+=contents[j][6]
            c+=1

    for j in range(0,6):
        out[j]=out[j]/c
    dis,ind=neigh.kneighbors([out])
    ans[id]=[]
    for j in ind[0]:
      ans[id].append(content_id[j])
      if(len(ans[id])>=10):
          break
    # for j in content.index:
    #     ter[content["content_id"][j]]=math.sqrt(abs(out[0]-content["content_type"][j])+abs(out[1]-content["language"][j])+abs(out[2]-content["genre"][j])+abs(out[3]-content["duration"][j])+abs(out[4]-content["rating"][j])+abs(out[5]-content["episode_count"][j]))
        
    # sorted(ter.items(), key=lambda x: x[1])  
    # c=0
    # ans[i] =[]
    # for j,k in ter.items():
    #     c+=1
    #     ans[i].append(j)
    #     if(c>=10):
    #         break
  else:
    ans[id]=[]
    for j in content.index:
      ans[id].append(content_id[j])
      if(j>=10):
        break

with open('sample_submission.json', 'w', encoding='utf-8') as f:
  json.dump(ans, f, ensure_ascii=False, indent=4)
print(ans)