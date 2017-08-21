from flask import Flask
from labstack import Client, Level
import traceback

app = Flask(__name__)

# Initialize LabStack client and log service
client = Client('<API_KEY>')
log = client.log()
log.add_fields(app_id='1', app_name='crash-reporting')
log.dispatch_interval = 5

# Routes
@app.route('/crash', methods=['GET'])
def crash():
  raise Exception('fatal error')
  return '', 204

@app.route('/error', methods=['GET'])
def error():
  # Manually report non-fatal error
  try:
    raise Exception('non-fatal error')
  except Exception as e:
    log.error(message=str(e))
  return '', 204

@app.errorhandler(Exception)
def exception_handler(e):
  # Automatically report crash (fatal error)
  log.fatal(message=str(e), stack_trace=traceback.format_exc())
  return 'error', 500 

if __name__ == '__main__':
  app.run(port=1323)