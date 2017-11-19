from pyrevit import UI
from postern import Postern, request


app = Postern('testapp')


# POST /select/2413
@app.route('/select/<int:element_id>', methods=['POST'])
def select(uiapp, element_id):
    pass


# GET  /query?objtype=Wall
@app.route('/query')
def query(uiapp):
    objtype = request.args.get('objtype')
    if objtype == 'Wall':
        walls_data = [{'objtype': 'Wall',
                       'id': 100,
                       'properties': ['prop1', 'prop2', 'prop3']
                       }]

        return walls_data


# POST /testfunc/anotherlevel
# { "message": "This is the TaskDialog message." }
# GET  /testfunc/anotherlevel
@app.route('/testfunc/anotherlevel', methods=['GET', 'POST'])
def testfunc(uiapp):
    if request.method == 'POST':
        data = request.data
        UI.TaskDialog.Show('Postern App', data['message'])
    elif request.method == 'GET':
        somedata = {'somevalue': 18,
                    'somelist': [1, 2, 3, 'name'],
                    'someobj': {1: 2,
                                3: 4}
                    }
        return somedata


app.run()


from postern import rulemap
print(rulemap.get_rule('testapp', '/testfunc/anotherlevel', 'GET'))
print(rulemap.get_rule('testapp', '/testfunc/anotherlevel', 'POST'))
