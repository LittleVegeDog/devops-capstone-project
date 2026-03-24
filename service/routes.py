"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

# ... place you code here to LIST accounts ...
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List accounts
    This endpoint will list all Accounts that have been created
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    acct_list = [acct.serialize() for acct in accounts]

    app.logger.info("Returning [%s] accounts", len(acct_list))
    return jsonify(acct_list), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################

# ... place you code here to READ an account ...
@app.route("/accounts/<int:acct_id>", methods=["GET"])
def read_accounts(acct_id):
    """
    Reads an Account
    This endpoint will read an Account info based on the acct_id value that is requested
    """
    app.logger.info("Request to read an Account with id: %s", acct_id)

    resp = Account.find(acct_id)
    
    if not resp:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{acct_id}] could not be found.")
    
    return resp.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place you code here to UPDATE an account ...
@app.route("/accounts/<int:acct_id>", methods=["PUT"])
def update_accounts(acct_id):
    """
    Updates an Account
    This endpoint will update the data of an Account based on the acct_id value that is requested
    """
    update_acct = Account.find(acct_id)
    
    if not update_acct:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{acct_id}] could not be found.")
    
    update_acct.deserialize(request.get_json())
    update_acct.update()
    return update_acct.serialize(), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...
@app.route("/accounts/<int:acct_id>", methods=["DELETE"])
def delete_accounts(acct_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the acct_id value that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", acct_id)

    del_acct = Account.find(acct_id)
    if del_acct:
        del_acct.delete()

    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
