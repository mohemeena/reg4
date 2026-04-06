#-----------------------------------------------------------------------
# database.py
# Author: Amel Osman & Mohemeen Ahmed
#-----------------------------------------------------------------------
""" Database program that communicates with the reg3.py program to 
extract and output relevant class overviews or details. """
import sqlite3
import contextlib
import sys

#-----------------------------------------------------------------------
DATABASE_URL = 'file:reg.sqlite'
#-----------------------------------------------------------------------

def get_overviews(reg_input):
    """ Method that takes in an input of a desired course 
    and selects the overviews for those courses. After 
    selecting, outputs the formatted course overviews. """

    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
        isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                # Ensuring wildcard characters are treated ordinarily
                title = reg_input["title"]
                title = title.replace("\\", "\\\\")
                title = title.replace("%", "\\%")
                title = title.replace("_", "\\_")

                # Create a prepared statement and substitute values.
                stmt_str = '''
                    SELECT classid, coursenum, dept, area, title
                    FROM classes, courses, crosslistings
                    WHERE courses.courseid = classes.courseid
                    AND courses.courseid = crosslistings.courseid
                    AND dept LIKE ?
                    AND coursenum LIKE ?
                    AND area LIKE ?
                    AND title LIKE ? ESCAPE '\\'
                    ORDER BY dept ASC, coursenum ASC, classid ASC
                    '''

                cursor.execute(stmt_str, [f'%{reg_input["dept"]}%',
                f'%{reg_input["coursenum"]}%', f'%{reg_input["area"]}%',
                f'%{title}%'])

                table = cursor.fetchall()
                overviews_list = []

                # Creating proper output
                for row in table:
                    course_overview = {
                        'classid': row[0],
                        'dept': row[2],
                        'coursenum': row[1],
                        'area': row[3],
                        'title': row[4]
                    }
                    overviews_list.append(course_overview)


            reg_output = [True, overviews_list]
            return reg_output


    # Error messages for our Error HTML Page
    except sqlite3.OperationalError as dbnopen:
        print(f'{sys.argv[0]}: unable to open database file: {dbnopen}',
        file=sys.stderr)
        return [False, "A server error occurred. "
        "Please contact the system administrator."]
    except sqlite3.DatabaseError as corrupt:
        print(
            f'{sys.argv[0]}: unable to access database file: {corrupt}',
            file=sys.stderr)
        return [False, "A server error occurred. "
        "Please contact the system administrator."]


def get_details(classid):
    """ Method that takes in an input of a desired course 
    and selects the details for those courses. After 
    selecting, outputs the formatted course details. """

    try:
        with sqlite3.connect(DATABASE_URL + '?mode=ro',
            isolation_level=None, uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                # Create a prepared statement and substitute values.
                stmt_str1 = '''
                    SELECT classid, days, starttime, endtime, bldg, roomnum
                    FROM classes
                    WHERE classid = ?
                    '''

                cursor.execute(stmt_str1, [classid])
                table1 = cursor.fetchall()


                stmt_str2 = '''
                    SELECT courses.courseid, area, title, descrip,
                      prereqs, classid
                    FROM classes, courses, crosslistings
                    WHERE courses.courseid = classes.courseid
                    AND courses.courseid = crosslistings.courseid
                    AND classid = ?
                    '''

                cursor.execute(stmt_str2, [classid])
                table2 = cursor.fetchall()

                stmt_strdeptandnum = '''
                    SELECT dept, coursenum, courses.courseid, classid
                    FROM courses, crosslistings, classes
                    WHERE courses.courseid = classes.courseid
                    AND courses.courseid = crosslistings.courseid
                    AND classid = ?
                    ORDER BY dept ASC, coursenum ASC
                    '''
                cursor.execute(stmt_strdeptandnum, [classid])
                table3 = cursor.fetchall()

                stmt_strprof = '''
                    SELECT profname, classes.courseid, 
                    coursesprofs.courseid, classid
                    FROM profs, coursesprofs, classes
                    WHERE classes.courseid = coursesprofs.courseid
                    AND coursesprofs.profid = profs.profid
                    AND classid = ?
                    ORDER BY profname ASC
                   '''

                cursor.execute(stmt_strprof, [classid])
                table4 = cursor.fetchall()

                # Create list for departments and course nums
                deptcoursenums = []
                for row in table3:
                    dept_dict = {
                        'dept': row[0],
                        'coursenum': row[1],
                    }
                    deptcoursenums.append(dept_dict)

                # Create list for profnames
                profnames = []
                for row in table4:
                    profnames.append(row[0])

                course_details = {
                        'classid': table1[0][0],
                        'days': table1[0][1],
                        'starttime': table1[0][2],
                        'endtime': table1[0][3],
                        'bldg': table1[0][4],
                        'roomnum': table1[0][5],
                        'courseid': table2[0][0],
                        'deptcoursenums': deptcoursenums,
                        'area': table2[0][1],
                        'title': table2[0][2],
                        'descrip': table2[0][3],
                        'prereqs': table2[0][4],
                        'profnames': profnames
                     }

                reg_output = [True, course_details]
                return reg_output

    except IndexError:
        return [False, f"no class with classid {classid} exists"]

    except sqlite3.OperationalError as dbnopen:
        print(f'{sys.argv[0]}: unable to open database file: {dbnopen}',
        file=sys.stderr)
        return [False, "A server error occurred. "
        "Please contact the system administrator."]

    except sqlite3.DatabaseError as corrupt:
        print(f'{sys.argv[0]}: no such table: {corrupt}',
        file=sys.stderr)
        return [False, "A server error occurred. "
        "Please contact the system administrator."]
