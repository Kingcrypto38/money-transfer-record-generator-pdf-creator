from os import getenv
from dotenv import load_dotenv
from app import app

load_dotenv()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=getenv('PORT') or 5000, debug=True)
