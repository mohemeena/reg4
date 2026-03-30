#-----------------------------------------------------------------------
# reg4.py
# Authors: Amel Osman & Mohemeen Ahmed
#-----------------------------------------------------------------------
""" Flask program that communicates with database.py to import class
overviews and details, and outputs them to be displayed on the proper
HTML file. """
import flask
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Class Overviews Page (Home Page):
#-----------------------------------------------------------------------
@app.route('/', methods={'GET'})
@app.route('/classoverviews', methods={'GET'})
def classoverviews():
    """ Method that extracts overviews from the database and
    sends to the classoverviews.html file to be displayed. """

    # Get the department inquiry
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''

    if dept == '':
        prev_dept = ''
    else:
        prev_dept = dept

    # Get the course number inquiry
    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum = ''

    if coursenum == '':
        prev_coursenum = ''
    else:
        prev_coursenum = coursenum

    # Get the area inquiry
    area = flask.request.args.get('area')
    if area is None:
        area = ''

    if area == '':
        prev_area = ''
    else:
        prev_area = area

    # Get the title inquiry
    title = flask.request.args.get('title')
    if title is None:
        title = ''

    if title == '':
        prev_title = ''
    else:
        prev_title = title

    query = {
        'dept': dept,
        'coursenum': coursenum,
        'area': area,
        'title': title
    }

    overviews_output = database.get_overviews(query)

    # If the database query was successful, display with HTML
    if overviews_output[0] is True:
        # Convert to JSON
        json_doc = json.dumps(overviews_output[1])

        # Create response
        response = flask.make_response(json_doc)
        response.headers['Content-Type'] = 'application/json'

    # If it was not successful, send to the error page

       #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #

    else:
        html_code = flask.render_template('error.html',
            error_message = overviews_output[1])
        response = flask.make_response(html_code)

    # Set cookies
    response.set_cookie('prev_dept', prev_dept)
    response.set_cookie('prev_coursenum', prev_coursenum)
    response.set_cookie('prev_area', prev_area)
    response.set_cookie('prev_title', prev_title)

    return response


#-----------------------------------------------------------------------
# Course Details Page:
#-----------------------------------------------------------------------
@app.route('/regdetails', methods={'GET'})

def classdetails():
    """ Method that extracts classdetails from the database
    and sends to the regdetails.html file to be displayed. """

    # Getting previous searches from cookies
    prev_dept = flask.request.cookies.get('prev_dept')
    if prev_dept is None:
        prev_dept = ''

    prev_coursenum = flask.request.cookies.get('prev_coursenum')
    if prev_coursenum is None:
        prev_coursenum = ''

    prev_area = flask.request.cookies.get('prev_area')
    if prev_area is None:
        prev_area = ''

    prev_title = flask.request.cookies.get('prev_title')
    if prev_title is None:
        prev_title = ''

    classid = flask.request.args.get('classid')

       #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #
    # Handling missing classid error
    if classid is None or classid == '':
        html_code = flask.render_template(
            'error.html',
            error_message='missing classid'
        )
        response = flask.make_response(html_code)
        return response

    # Check if classid not integer
    try:
        int(classid)
    except Exception:
        html_code = flask.render_template(
            'error.html',
            error_message='non-integer classid'
        )
        response = flask.make_response(html_code)
        return response

    details_output = database.get_details(classid)

    # If the database query was successful, display with HTML
    if details_output[0] is True:

        # Convert to JSON
        json_doc = json.dumps(details_output[1])

        # Create response
        response = flask.make_response(json_doc)
        response.headers['Content-Type'] = 'application/json'

    # If it was not successful, send to the error page
    else:
        #
        #
        #
         ## HANDLE ERRORS ##
        #
        #
        #
        html_code = flask.render_template('error.html',
            error_message = f'no class with classid {classid} exists')
        response = flask.make_response(html_code)

    return response
