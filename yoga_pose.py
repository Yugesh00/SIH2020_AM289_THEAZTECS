import numpy as np
from .root import app

DO_NOT_KNOW = "Looks like I need to study for this yoga pose."

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


@app.handle(intent='yoga_pose', has_entity='other_names')
def get_other_names(request, responder):
    responder = _get_yoga_pose(request, responder, 'other_names')
    try:
        responder.reply("Other names for {name} are {other_names} ")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
    return

@app.handle(intent='yoga_pose', has_entity='pose_description')
def get_pose_description(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_description')
    try:
        responder.reply("{pose_description}")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return


@app.handle(intent='yoga_pose', has_entity='pose_steps')
def get_pose_steps(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_steps')
    try:
        responder.reply("Steps for {name} are: {pose_steps}")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return


@app.handle(intent='yoga_pose', has_entity='pose_release')
def get_pose_release(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_release')
    try:
        responder.reply("{pose_release}")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return


@app.handle(intent='yoga_pose', has_entity='pose_benefits')
def get_pose_benefits(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_benefits')
    try:
        responder.reply("Benefits for {name} are {pose_benefits}")        
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return


@app.handle(intent='yoga_pose', has_entity='pose_precautions')
def get_pose_precautions(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_precautions')
    try:
        responder.reply("{pose_precautions}")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return

@app.handle(intent='yoga_pose', has_entity='pose_links')
def get_pose_links(request, responder):
    responder = _get_yoga_pose(request, responder, 'pose_links')
    try:
        responder.reply("You can watch video for {name} here {pose_links}")
    except KeyError:
        responder.reply(DO_NOT_KNOW)
        return

# Default case
@app.handle(intent='yoga_pose')
def get_info_default(request, responder):


    try:
        name_ent = extract_entities_from_type(request, 'pose_name')
        name = name_ent[0]['value'][0]['cname']

        if name == '':
            responder.reply(DO_NOT_KNOW)
            return

        responder.frame['name'] = name
        responder.frame['info_visited'] = True
        responder.slots['name'] = name
        responder.reply("What would you like to know about {name}? ")
        

    except (KeyError, IndexError):

        if request.frame.get('info_visited'):
            name = request.frame.get('name')
            responder.slots['name'] = name

            pose = app.question_answerer.get(index='yoga_pose', pose_name=name)
            if pose:
                details = pose[0]

                expand_dict = {'other_names': 'Other Names', 'pose_description': 'Description for the pose',
                               'pose_steps': 'Steps for the pose', 'pose_release': 'Release pose',
                               'pose_precautions': 'Preacautions'}
                details = [str(expand_dict[key]) + " : " + str(details[key])
                           for key in details.keys()
                           if key in expand_dict]

                responder.slots['details'] = '; '.join(details)
                responder.reply("I found the following details about {name}: {details}")
                responder.frame = {}

            else:
                replies = ["Hmmm, looks like I don't know about this yoga pose yet! "
                           "Would you like to know about some other yoga pose?"]
                responder.reply(replies)
                responder.frame = {}
        else:
            responder.reply("I believe, I need to study regarding this yoga pose.")
            responder.frame['info_visited'] = False



def _get_yoga_pose(request, responder, entity_type):

    name = request.frame.get('pose_name')
    try:
        name_ent = extract_entities_from_type(request, 'pose_name')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder
    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder




def _fetch_from_kb(responder, name, entity_type):

    poses = app.question_answerer.get(index='yoga_pose', pose_name=name)
    entity_option = poses[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder
