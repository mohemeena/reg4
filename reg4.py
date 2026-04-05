#-----------------------------------------------------------------------
# reg4.py
# Authors: Amel Osman & Mohemeen Ahmed
#-----------------------------------------------------------------------
""" Flask program that communicates with database.py to import class
overviews and details, and outputs them to be displayed on the proper
HTML file. """
import flask
import database
import json

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Home Page
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    return flask.send_file('index.html')

#-----------------------------------------------------------------------
# Class Overviews Results 
#-----------------------------------------------------------------------
@app.route('/searchresults', methods=['GET'])
def search_results():
    """ Method that extracts overviews from the database and
    sends to the classoverviews.html file to be displayed. """

    # Get the department inquiry
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''
    dept = dept.strip()

    # Get the course number inquiry
    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum = ''
    coursenum = coursenum.strip()

    # Get the area inquiry
    area = flask.request.args.get('area')
    if area is None:
        area = ''
    area = area.strip()

    # Get the title inquiry
    title = flask.request.args.get('title')
    if title is None:
        title = ''

    query = {
        'dept': dept,
        'coursenum': coursenum,
        'area': area,
        'title': title
    }

    overviews_output = database.get_overviews(query)
    overviews = overviews_output[1]

    json_doc = json.dumps(overviews)
    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'
    return response

    # If the database query was successful, display with HTML
    #if overviews_output[0] is True:
        # Convert to JSON
       # json_doc = json.dumps(overviews_output[1])

        # Create response
        #response = flask.make_response(json_doc)
        #response.headers['Content-Type'] = 'application/json'

    # If it was not successful, send to the error page

       #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #

    #else:
        #html_code = flask.render_template('error.html',
            #error_message = overviews_output[1])
        #response = flask.make_response(html_code)


#-----------------------------------------------------------------------
# Course Details Page:
#-----------------------------------------------------------------------
@app.route('/regdetails', methods=['GET'])
def regdetails():
    """ Method that extracts classdetails from the database
    and sends to the regdetails.html file to be displayed. """

    classid = flask.request.args.get('classid')

       #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #
    # Handling missing classid error
    #if classid is None or classid == '':
        #html_code = flask.render_template(
            #'error.html',
            #error_message='missing classid'
        #)
        #response = flask.make_response(html_code)
        #return response

    # Check if classid not integer
    #try:
        #int(classid)
    #except Exception:
        #html_code = flask.render_template(
            #'error.html',
            #error_message='non-integer classid'
        #)
        #response = flask.make_response(html_code)
        #return response

    details_output = database.get_details(classid)
    # Convert to JSON
    json_doc = json.dumps(details_output[1])

    # Create response
    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'

    # If it was not successful, send to the error page
    #else:
        #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #
        #html_code = flask.render_template('error.html',
            #error_message = f'no class with classid {classid} exists')
        #response = flask.make_response(html_code)

    return response
