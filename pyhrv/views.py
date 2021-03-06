from tojson import render_to_json
from collections import defaultdict
#from .utils import 
import psycopg2
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
import socket
from django.shortcuts import render
from datetime import datetime
from time import strftime
import json
from .models import SubmittedProcess
from .utils import RetrieveOnLineWorkFlows, ExecuteMonitoringDaemon
from multiprocessing import Process, Queue

   
def MainView(request):
    template_name = 'pyhrv/home.html'
    return render(request, 'pyhrv/home.html')

@render_to_json()        
def process_key(request):
    key = request.POST.get('key',None)
    pipelines = []
    users = []
    sub_proc = []
    results = []
    host = 'mpbagalaxy.fbk.eu'
    try:
        pipelines = RetrieveOnLineWorkFlows(host,key)
    except Exception, e:
        print e
        pipelines = "Error retrieving the API key: check if it is correct"
    try:
        conn = psycopg2.connect("dbname='hrv_realtime' user='geopgdbmgr' host='geopg' password='geo2K12pg!!'")
        cur=conn.cursor()
        cur.execute("SELECT * from subjects")
        users = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    except Exception, e:
        print e
    try:    
        sub_procs = SubmittedProcess.objects.filter(galaxy_key=key)
        #sub_proc = SubmittedProcess.objects.all()
    except Exception, e:
        print "db exception "+e
    for proc in sub_procs:
        sub_proc.append({'user': proc.user , 'pipeline': proc.pipeline, 'status': proc.status, 'submitted':proc.submitted , 'id': proc.process_id, 'user_id':proc.user_id, 'pipe_id': proc.pipeline_id, 'key': proc.galaxy_key})
    #sub_proc.append({'user':'user1', 'pipeline':'pipe3', 'status':True, 'submitted':date, 'id':2, 'user_id':'1', 'pipe_id':'3', 'key':key})
    results.append({'pipelines':pipelines})
    results.append({'users':users})
    results.append({'sub_proc':list(sub_proc)})
    return results

@render_to_json()
def submit_jobs(request):
    pipe_list = json.loads(request.POST.get('pipeline_list', []))
    user_list = json.loads(request.POST.get('user_list', []))
    key = request.POST.get('key', None)
    host = 'mpbagalaxy.fbk.eu'
    sub_jobs =[]
    warn = False
    key = request.POST.get('key',None)
    for pipe in pipe_list:
        for usr in user_list:
            try:
                SubmittedProcess.objects.filter(galaxy_key=key, user_id=usr['id'], pipeline_id=pipe['id'])
                warn = True
            except Exception, e:
                print e
            try:        
                p = Process(target=ExecuteMonitoringDaemon, args=(host,key, pipe['id'], usr['name'],))
                p.start()
                print p.pid
                submitted = True  
            except Exception, e:
                print e    
            if submitted == True:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sub=SubmittedProcess(galaxy_key=key, pipeline=pipe['name'], user=usr['name'], pipeline_id=pipe['id'], user_id=usr['id'] , status="running", submitted=date)
                try:
                    sub.save()
                    pid = sub.process_id
                except Exception, e:
                    print e
            sub_jobs.append({'pipeline':pipe['name'], 'user':usr['name'], 'user_id':usr['id'], 'pipe_id':pipe['id'], 'key': key, 'status':submitted, 'warn':warn, 'submitted':date, 'process_id':pid})                
    return sub_jobs

@render_to_json()
def start_process(request):
    job_id = request.POST.get('job_id', None)
    key = request.POST.get('key',None)
    sub_proc = SubmittedProcess.objects.get(process_id=job_id)
    host = 'mpbagalaxy.fbk.eu'
    print sub_proc
    try:    
        p = Process(target=ExecuteMonitoringDaemon, args=(host,key, sub_proc.pipeline_id, sub_proc.user,))
        p.start()  
    except Exception, e:
        print e     
    return {'status' : 'success'}

@render_to_json()
def stop_process(request):
    job_id = request.POST.get('job_id', None)
    key = request.POST.get('key',None)      
    stopped = True #######################
    return {'status' : 'success'}
