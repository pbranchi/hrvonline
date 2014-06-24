from bioblend.galaxy import GalaxyInstance


def RetrieveOnLineWorkFlows(host='http://laske.fbk.eu:50001',api_key='33416687e72abf376c4860b7ab18e1f5'):
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
