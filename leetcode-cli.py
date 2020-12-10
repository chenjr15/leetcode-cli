#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass

import click

# TODO tempelate code
# TODO problem description

@dataclass
class QuestionStat:
    ''' '''
    question_id:int
    question__title:str
    question__title_slug: str
    question__article__live:str
    question__article__slug:str
    question__hide: bool
    total_acs: int
    total_submitted: int
    frontend_question_id: int
    is_new_question: bool
    total_column_articles:int
    @property
    def dir_name(self):
        return f"{self.frontend_question_id}-{self.question__title_slug}"
    
    def src_full_pah(self,ext = "go"):
        return f"{self.question__title_slug.replace('-','_')}.{ext}"

    def makedir(self):
        path = os.path.join(os.path.abspath(os.curdir),self.dir_name)
        filepath = os.path.join(path,self.src_full_pah())
        try:
            os.stat(path)
            # print(f"Exists {path}")
        except FileNotFoundError:
            print(f"Making {path}",file=sys.stderr)
            os.mkdir(path)
        with open(filepath,"w",encoding='utf-8') as f:
            f.write(f"package leetcode{self.frontend_question_id}\n")
        return path
    def __str__(self):
        return f'#{self.frontend_question_id} {self.question__title} {self.question__title_slug}'

def load_questions(question_json="problem.json"):
    
    with open(question_json) as f:
        data = json.load(f)
    with open(question_json+".idented.json","w") as f:
        json.dump(data,f,indent=2)
    pairs= data["stat_status_pairs"]
    q_map = {}
    for q in pairs:
        question = QuestionStat(**q["stat"])
        q_map[question.frontend_question_id] = question
    return q_map 

def load_keywords(question_map:map,cache_file_path:str = "keywords_index.json")->map:
    print(os.getcwd(),cache_file_path)
    keywords_map= {}
    if os.path.exists(cache_file_path):
        with open(cache_file_path) as f:
            keywords_map = json.load(f)
        return keywords_map

    for q in question_map.values():
        kws = [kw.lower() for kw in q.question__title.split()]
        for kw in kws:
            keywords_map.setdefault(kw,set()).add(q.frontend_question_id)

    with open(cache_file_path,"w") as f:
        def set_default(obj):
            if isinstance(obj,set):
                return list(obj)
            raise TypeError
        json.dump(keywords_map,f,default=set_default)

    return keywords_map 

@click.command()
@click.option('-p','--path',help="code path of leetcode,could be set by Environment Variables LEETCODE_PATH")
@click.option('-j','--question_json',default=lambda :os.path.expanduser('~/.config/leetcode-cli/problem.json'),help="")
@click.option('-c','--keywords_json',default=lambda :os.path.expanduser('~/.config/leetcode-cli/keywords.json'),help="keywords index cache json")
@click.option('-k','--keyword',help="to search problem title with a single keyword")
@click.option('-s','--search',is_flag =True, default=False,help="to search problem title")
@click.argument('qid',default=0,type=click.types.INT)
def leetcode(qid:int=0,path:str=None,question_json = 'problem.json',keyword:str=None,search=False,keywords_json='keywords.json' ):
    if path :
        os.chdir(path)
    question_map=load_questions(question_json)

    if keyword:
        keyword = keyword.lower()
        keywords_map = load_keywords(question_map,keywords_json)
        if keyword not in keywords_map:
            print("NO MATCH for",keyword)
            return 
        for qid in  keywords_map[keyword]:
            q =question_map[qid]
            print(q)

        return
    if search:
        search= input("Search:").lower()
        releated = []
        for q in question_map.values():
            if search in q.question__title.lower():
                releated.append(q)
        for q in releated:
            print(q)
        return
    if not qid:
        print(os.path.abspath(os.curdir))
        return
    try:
        q = question_map[qid]
    except IndexError:
        print(f"Question with id {qid} Not Exists!",file=sys.stderr)
        return
    path = q.makedir()
    print(path)
    

if __name__ == "__main__":
    
    leetcode(auto_envvar_prefix ="leetcode")

