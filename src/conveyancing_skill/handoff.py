"""Export workflow actions for a human-controlled case-system import."""
import csv
from pathlib import Path
from .engine import LegalReviewRequired


def export_actions(workflow, destination):
    if not isinstance(workflow,dict) or not isinstance(workflow.get('stages'),list):
        raise LegalReviewRequired('Expected a workflow object with stages')
    rows=[]
    for stage in workflow['stages']:
        if not isinstance(stage,dict) or not isinstance(stage.get('work_record'),dict):
            raise LegalReviewRequired('Stage missing work_record')
        actions=stage['work_record'].get('open_actions',[])
        if not isinstance(actions,list): raise LegalReviewRequired('open_actions must be a list')
        for index,action in enumerate(actions,1):
            if not isinstance(action,dict): raise LegalReviewRequired('Action must be an object')
            rows.append([stage.get('id',''),str(index),stage.get('title',''),action.get('action',''),
                         action.get('status','outstanding'),action.get('owner'),action.get('due_date')])
    def safe(value):
        text='' if value is None else str(value)
        return "'"+text if text.lstrip().startswith(('=','+','-','@')) or text.startswith(('\t','\r','\n')) else text
    path=Path(destination)
    try:
        with path.open('x',encoding='utf-8-sig',newline='') as f:
            writer=csv.writer(f);writer.writerow(['stage_id','action_number','stage_title','action','status','owner','due_date'])
            writer.writerows([[safe(x) for x in row] for row in rows])
    except FileExistsError as exc:
        raise LegalReviewRequired('Export destination already exists; choose a new file') from exc
    return {'output':str(path),'rows':len(rows),'status':'EXPORTED_FOR_HUMAN_REVIEW','note':'Local CSV only; no case system has been updated. Confirm field mapping and use approved matter storage.'}
