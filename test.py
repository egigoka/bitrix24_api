from commands import *
from bitrix24api import BitrixRESTAPI

hook = "https://kurganmk.bitrix24.ru/rest/11/tbjn4luh6u1b6irw/"
b24 = BitrixRESTAPI(hook)

task = {"task": {"id": 2525}}
comment = "test"

response = b24.post('task.commentitem.add.json', [task["task"]["id"], {'POST_MESSAGE': comment}], verbose=True)
Print.prettify(response)