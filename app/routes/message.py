from flask import Blueprint, render_template


message_view = Blueprint("message_blueprint", __name__)

@message_view.route('/message')
def chat_view():
    return render_template("chat/chat_view.html")
