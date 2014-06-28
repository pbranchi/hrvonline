from bioblend.galaxy import GalaxyInstance


def RetrieveOnLineWorkFlows(host,api_key):
    gi = GalaxyInstance(host, key=api_key)

    wf = gi.workflows.get_workflows()

    online_ws = []

    for item in wf:
        id_wf = item['id']
        id_name = item['name']
        wf_det = gi.workflows.show_workflow(id_wf)

        online_input = False
        online_output = False
        for k,v in wf_det['steps'].items():
            if v['tool_id'] == 'hrv_online_outputgenerator':
                online_output = True
            if v['tool_id'] == 'hrv_online_inputreader':
                online_input = True

        if online_output and online_input:
            online_ws.append((id_wf,id_name))

    return online_ws

def ExecuteMonitoringDaemon(host,api_key, workflow_id, subject_name):


    gi = GalaxyInstance(host, key=api_key)
    curr_hist = gi.histories.get_current_history()
    hist_id = curr_hist['id']
    ds_output = gi.tools.run_tool(history_id=hist_id, tool_id='hrv_online_daemon', tool_inputs={'subject_name':subject_name, 'workflow_id':workflow_id})
    print ds_output.values()[0][0]['id']


    return True    
