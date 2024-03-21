import itertools
from collections import defaultdict
import time
second = time.time()
debugl=[]
debugd={}
class Node:
    def __init__(self, item, freq, father):
        self.item = item
        self.freq = freq
        # 父節點指標
        self.father = father
        # 定義指標
        self.link = None
        # 孩子節點，用dict儲存，方便根據item查詢
        self.children = {}
    
    # 更新頻次
    def update_freq(self,add=1):
        self.freq += add

    # 新增孩子
    def add_child(self, node):
        self.children[node.item] = node


def creat_data():
  f=open("python.data.txt")
  l=[]
  for i in f.readlines():
    i=i.split(" ")
    l1=[]
    for j in i:
      if j != "\n":
        l1.append(int(j))
    l.append(l1)
  return l

def creat_init_dict(data,at_least):
  d={}
  for i in data:
    for j in i:
      if j in d:
        d[j]+=1
      else:
        d[j]=1
  d1={}
  for i in d.keys():
    if d[i]>=at_least:
      d1[i]=d[i]
  d1={k: v for k, v in sorted(d1.items(), key=lambda item: item[1],reverse=True)}
  return d1

def creat_head(init_dict):
  return {k:[v,None,None] for k,v in init_dict.items()}

def creat_need_data(data,init_dict):
  l=[]
  for i in data:
    l1=[]
    for j,k in init_dict.items():
      if j in i:
        l1.append(j)
    l.append(l1)
  return l

def creat_fp_tree(need_data,head_dict):
  root=Node("NULL",0,None)
  for i in need_data:
    now=root
    for j in i:
      if j in now.children:
        now=now.children[j]
        now.update_freq()

      else:
        tmp=Node(j,1,now)
        now.add_child(tmp)
        now=tmp
        if head_dict[j][1] is None:
          head_dict[j][1]=tmp
          head_dict[j][2]=tmp
        else:
          head_dict[j][2].link=tmp
          head_dict[j][2]=tmp
          
  return root

def creat_fp_tree_1(need,l,d):
  nroot=Node("NULL",0,None)
  id=0
  for i in need:
    now=nroot
    for j in i:
      if j in now.children:
        now=now.children[j]
        now.update_freq(l[id])
      else:
        tmp=Node(j,l[id],now)
        now.add_child(tmp)
        now=tmp
        if d[j][1] is None:
          d[j][1]=tmp
          d[j][2]=tmp
        else:
          d[j][2].link=tmp
          d[j][2]=tmp
    id+=1
          
  return nroot

def dfs(head_dict,at_least,f,s,num_dict):
  sorted_items=[k for k in head_dict if head_dict[k][0] >= at_least]
  sorted_items.sort(key=lambda x: head_dict[x][0])
  for i in sorted_items:
    need, l=[], []
    s_new = s.copy()
    s_new.add(i)
    num_dict[len(s_new)]+=1
    if frozenset(s_new) not in f:
      f[frozenset(s_new)]=head_dict[i][0]
    else:
      f[frozenset(s_new)]+=head_dict[i][0]
    d=defaultdict(int)
    now=head_dict[i][1]
    while now != None:
      nownode=now.father
      tmp=[]
      d1=defaultdict(int)
      while nownode != None:
        if nownode.item == "NULL":
          break
        tmp.append(nownode.item)
        d1[nownode.item]+=1
        nownode=nownode.father
      for i,j in d1.items():
        d[i]+=now.freq
      tmp=reversed(tmp)
      need.append(tmp)
      l.append(now.freq)#通靈
      now=now.link
    d=creat_head(d)
    newroot=creat_fp_tree_1(need,l,d)
    if len(newroot.children)!=0 and len(s_new)<5:
      dfs(d,at_least, f, s_new,num_dict)

def creat_association_rule(freq_list,confidence):
  ans=0
  for i,j in freq_list.items():
    if len(i)>=2:
      for k in itertools.combinations(i,1):
        l=[k[0]]
        if (j/freq_list[frozenset(l)])>=confidence:
          ans+=1
    if len(i)>=3:
      for k in itertools.combinations(i,2):
        l=[k[0],k[1]]
        if (j/freq_list[frozenset(l)])>=confidence:
          ans+=1
    if len(i)>=4:
      for k in itertools.combinations(i,3):
        l=[k[0],k[1],k[2]]
        if (j/freq_list[frozenset(l)])>=confidence:
          ans+=1
    if len(i)>=5:
      for k in itertools.combinations(i,4):
        l=[k[0],k[1],k[2],k[3]]
        if (j/freq_list[frozenset(l)])>=confidence:
          ans+=1
  return ans

if __name__=="__main__":
  data=creat_data()
  #print(len(data))
  #data=[[1,2,5],[2,4],[2,3],[1,2,4],[1,3],[2,3],[1,3],[1,2,3,5],[1,2,3]]
  init_dict=creat_init_dict(data,813)
  head_dict=creat_head(init_dict)
  #print(init_dict)
  need_data=creat_need_data(data,init_dict)
  root=creat_fp_tree(need_data,head_dict)
  #check_fp_tree(root,need_data,init_dict)
  num_dict={}
  num_dict[1]=0
  num_dict[2]=0
  num_dict[3]=0
  num_dict[4]=0
  num_dict[5]=0
  freq_list={}
  dfs(head_dict,813, freq_list, set(),num_dict)
  print(num_dict)
  print(creat_association_rule(freq_list,0.8))
  end=time.time()
  print(end-second,end=" 秒")