from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory
import x
import uuid # 36 decimals (32 no dash)
import time # EPOCH, timestamp
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
 
from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)
 
app = Flask(__name__)
 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# ic(int ( time.time() ) )

@app.route('/dist/<path:filename>')
def serve_dist(filename):
    return send_from_directory('dist', filename)


###############################################  GET HOMEPAGE  #########################################################

@app.get("/")
@x.no_cache
def show_homepage():
    try:
        user = session.get("user", "")
        return render_template("page_index.html", user=user)

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500



#############################################  GET SIGNUP PAGE  #######################################################

@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500



#################################  OPRET/POST A USER INTO __form_signup.html  #########################################

@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        user_hashed_password = generate_password_hash(user_password)

        # ic(user_hashed_password) 'scrypt:32768:8:1$c2kPewCjWJ6Ltcbw$98749092e39a0d598ad58dbab62dc024c3a3252be9e0bddacea001d457ca7aa6d4742bddca2efc3d02b91739ef13d4e06eacf5ef8341901a68b82490de524f0e'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        # Create a variable for the form microtemplate, to show instead of previous filled out form
        form_signup = render_template("___form_signup.html", x=x)

        return f"""
            <browser mix-replace="form">{form_signup}</browser>
            <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)
        # If statement for first name
        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for last name
        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for email
        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for password
        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for duplicated email
        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exist"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400


        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500
        
    finally: 
        if "cursor" in locals(): cursor.close() # Locals refers to anything inside the try or except
        if "db" in locals(): db.close() # db refers to anything inside the database



#############################################  GET LOGIN PAGE  #######################################################

@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        # If not correct user, redirect to login page
        if not user: 
            return render_template("page_login.html", user=user, x=x)

        # If the user is logged in, redirect to profile page
        return redirect("/profile")

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500



#################################  INDSÆT USER IN FORM AND CHECK IN DATABASE  #########################################

@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        # Check if the user is in the system
        if not user:
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        # Check if the password in database match the password input field
        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400


        # Make sure the password is not saved in the terminal/system
        user.pop("user_password")

        # If everything went correct, the user equals the user in the database
        session["user"] = user

        # Redirect the user to the profile page
        return f"""<browser mix-redirect="/profile"></browser>"""


    except Exception as ex:
        ic(ex)

        # If statement for email
        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for password
        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400


        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500
        
    finally: 
        if "cursor" in locals(): cursor.close() # Locals refers to anything inside the try or except
        if "db" in locals(): db.close() # db refers to anything inside the database
      


#############################################  GET LOGOUT PAGE  #######################################################

@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500



#######################################  GET ALL DESTINATIONS PAGE  ###################################################

@app.get("/all-destinations")
@x.no_cache
def show_all_destinations():
    try:
        user = session.get("user", "")
        db, cursor = x.db()
        q = "SELECT * FROM destinations"
        cursor.execute(q)
        destinations = cursor.fetchall()
        return render_template("page_all_destinations.html", destinations=destinations, user=user)

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



######################################  GET CREATE DESTINATION PAGE  ##################################################

@app.get("/create-destination")
@x.no_cache
def show_create_destination():
    try:
        user = session.get("user", "")
        if not user:
            return redirect("/login")
        return render_template("page_create_destination.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500



########################  OPRET/POST A DESTINATION INTO page_create_destination.html  #################################

@app.post("/api-create-destination")
def api_create_destination():
    try:
        destination_title = x.validate_destination_title()
        destination_country = x.validate_destination_country()
        destination_location = x.validate_destination_location()
        destination_description = request.form.get("destination_description", "")
        destination_date_from = request.form.get("destination_date_from", "")
        destination_date_to = request.form.get("destination_date_to", "")

        # Get the logged user as user_fk
        user = session.get("user")
        user_fk = user["user_pk"]

        destination_pk = uuid.uuid4().hex
        destination_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO destinations VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(q, (destination_pk, destination_title, destination_description, destination_country, destination_location, destination_created_at, destination_date_from, destination_date_to, user_fk))
        db.commit()

        return f"""<browser mix-redirect="/all-destinations"></browser>"""


    except Exception as ex:
        ic(ex)

        # If statement for destination title
        if "company_exception destination_title" in str(ex):
            error_message = f"Destination title {x.DESTINATION_TITLE_MIN} to {x.DESTINATION_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for destination country
        if "company_exception destination_country" in str(ex):
            error_message = "Country invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for destination location
        if "company_exception destination_location" in str(ex):
            error_message = "Location invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

        
    finally: 
        if "cursor" in locals(): cursor.close() # Locals refers to anything inside the try or except
        if "db" in locals(): db.close() # db refers to anything inside the database



#############################################  GET PROFILE PAGE  #######################################################

@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")

        # If there is no user, redirect to login page
        if not user:
            return redirect("/login")
        
        db, cursor = x.db()
        q = "SELECT * FROM destinations WHERE user_fk = %s"
        cursor.execute(q, (user["user_pk"],))
        destinations = cursor.fetchall()

        # If the user is logged in, stay in profile page (CANT go to login again if already logged in)
        return render_template("page_profile.html", user=user, destinations=destinations, x=x)

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



#######################################  GET EDIT DESTINATION PAGE  ###################################################

@app.get("/edit-destination/<destination_pk>")
@x.no_cache
def show_edit_destination(destination_pk):
    try:
        user = session.get("user", "")

        # If there is no user, redirect to login page
        if not user:
            return redirect("/login")

        db, cursor = x.db()
        q = "SELECT * FROM destinations WHERE destination_pk = %s AND user_fk = %s"
        cursor.execute(q, (destination_pk, user["user_pk"]))
        destination = cursor.fetchone()

        # If destination not found or doesn't belong to user
        if not destination:
            return "not allowed", 403

        return render_template("page_edit_destination.html", destination=destination, user=user, x=x)

    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



############################  EDIT A DESTINATION FROM PROFILE IN page_profile.html  ###################################

@app.patch("/api-update-destination/<destination_pk>")
def api_update_destination(destination_pk):
    try:
        destination_title = x.validate_destination_title()
        destination_country = x.validate_destination_country()
        destination_location = x.validate_destination_location()
        destination_description = request.form.get("destination_description", "")
        destination_date_from = request.form.get("destination_date_from", "")
        destination_date_to = request.form.get("destination_date_to", "")

        # Get the logged user to verify ownership
        user = session.get("user")
        user_fk = user["user_pk"]

        db, cursor = x.db()
        q = """UPDATE destinations SET
                destination_title = %s,
                destination_description = %s,
                destination_country = %s,
                destination_location = %s,
                destination_date_from = %s,
                destination_date_to = %s
               WHERE destination_pk = %s AND user_fk = %s"""

        cursor.execute(q, (destination_title, destination_description, destination_country, destination_location, destination_date_from, destination_date_to, destination_pk, user_fk))
        db.commit()

        return f"""<browser mix-redirect="/profile"></browser>"""


    except Exception as ex:
        ic(ex)

        # If statement for destination title
        if "company_exception destination_title" in str(ex):
            error_message = f"Destination title {x.DESTINATION_TITLE_MIN} to {x.DESTINATION_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for destination country
        if "company_exception destination_country" in str(ex):
            error_message = "Country invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # If statement for destination location
        if "company_exception destination_location" in str(ex):
            error_message = "Location invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



###########################  DELETE A DESTINATION FROM PROFILE IN page_profile.html  ##################################

@app.delete("/api-delete-destination/<destination_pk>")
def api_delete_destination(destination_pk):
    try:
        user = session.get("user")

        # If there is no user, redirect to login page
        if not user:
            return redirect("/login")

        db, cursor = x.db()
        q = "DELETE FROM destinations WHERE destination_pk = %s AND user_fk = %s"
        cursor.execute(q, (destination_pk, user["user_pk"]))
        db.commit()

        return f"""<browser mix-redirect="/profile"></browser>"""


    except Exception as ex:
        ic(ex)
        return "system under maintenance", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()




