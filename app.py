from os import getenv
from dotenv import load_dotenv
from flask import Flask, make_response, send_file, render_template, request, abort
import pdfkit

load_dotenv()
app = Flask(__name__)

@app.route("/pdf", methods=["POST"])
def pdf():
  if request.headers.get('Authorization') == getenv("AUTH"):
    try :
      transactions = request.json['transactions']
      statementNumber = request.json['statementNumber']
      date = request.json['date']
    except:
      abort(416)
    for transaction in transactions:
      try:
        _ = int(transaction['transactionNumber'])
        _ = float(transaction['amount'])
        _ = str(transaction['place'])
        _ = str(transaction['benefitiaryName'])
        _ = str(transaction['senderName'])
      except:
        abort(406)
    rendered = render_template('main.html', transactions=transactions, statementNumber=statementNumber, date=date)
    options = {
      'page-size': 'A4',
      'margin-top': '0.50in',
      'margin-right': '0.40in',
      'margin-bottom': '0.50in',
      'margin-left': '0.40in',
      'encoding': "UTF-8",
    }
    stylesheetsPath = 'static/stylesheets'
    css = [
      '{}/rtl-bootstrap.min.css'.format(stylesheetsPath),
      '{}/main.css'.format(stylesheetsPath)
    ]
    pdf = pdfkit.from_string(rendered, False, options=options, css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;'
    return response
  else:
    abort(401)

# Catch all route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  abort(403)