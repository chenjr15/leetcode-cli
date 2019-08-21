#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass

import click


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

@click.command()
@click.option('-p','--path',help="code path of leetcode,could be set by Environment Variables LEETCODE_PATH")
@click.option('-j','--question_json',default=lambda :os.path.expanduser('~/.config/leetcode-cli/problem.json'),help="")
@click.argument('qid',default=0,type=click.types.INT)
def leetcode(qid:int=0,path:str=None,question_json = 'problem.json'):
    if path :
        os.chdir(path)
    if not qid:
        print(os.path.abspath(os.curdir))
        return
    question_list=load_questions(question_json)
    try:
        q = question_list[qid]
    except IndexError:
        print(f"Question with id {qid} Not Exists!",file=sys.stderr)
        return
    path = q.makedir()
    print(path)
    

if __name__ == "__main__":
    
    leetcode(auto_envvar_prefix ="leetcode")

