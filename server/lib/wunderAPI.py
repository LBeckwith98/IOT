import requests
import json


access_token = 'ccbbd1f334b31f538c2f5a991627ea247f35ce363a730b7a575d5b24e772'
client_id = '58a2538d72198ee701dd'
list_id = '348748343'

headers={'X-Access-Token': access_token, 'X-Client-ID': client_id, 'Content-Type' : 'application/json'}


def pollWunder():
    #response = requests.get('https://a.wunderlist.com/api/v1/tasks', headers=headers, params={'list_id': list_id})
    #msg = json.loads(response.text)
    #return processMsg(msg)
    return ["NONE"]


def processMsg(msg):
    command = ["NONE"]  # [Destination, Command, args...]

    ## ALARM CLOCK MESSAGES ##
    for task in msg:

        # set alarm : hr:min
        if task['title'].replace(':',' ').split(' ')[0].lower() == 'set' and task['title'].split(' ')[1].lower() == 'alarm':
            command[0] = "ALARM_CLOCK"
            command.append("UPDATE_ALARM")
            try:
                command.append(task['title'].replace(':',' ').split(' ')[2])
                command.append(task['title'].replace(':',' ').split(' ')[3])
                requests.delete('https://a.wunderlist.com/api/v1/tasks/' + str(task['id']),
                          headers=headers, params={'revision': 1})
            except:
                return ["NONE"]

        # light on
        elif task['title'].lower() == 'light on':
            command[0] = "ALARM_CLOCK"
            command.append("TURN_ON_LIGHT")
            requests.delete('https://a.wunderlist.com/api/v1/tasks/' + str(task['id']),
                            headers=headers, params={'revision': 1})
        # light off
        elif task['title'].lower() == 'light off':
            command[0] = "ALARM_CLOCK"
            command.append("TURN_OFF_LIGHT")
            requests.delete('https://a.wunderlist.com/api/v1/tasks/' + str(task['id']),
                            headers=headers, params={'revision': 1})
    return command

