from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from controller import *

def checkParam(path, newPath):
  pathArray = path.split('/')
  newPathArray = newPath.split('/')
  paramsMap = {}
  if len(pathArray) != len(newPathArray):
    return False
  for index in range(len(pathArray)):
    if pathArray[index] != newPathArray[index]:
      if len(pathArray[index]) == 0 or pathArray[index][0] != ':':
        return False
      paramsMap[pathArray[index]] = newPathArray[index]
  return paramsMap

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
      logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
      self._set_response()
      if self.path == '/sectors':
        sectors = json.dumps(getAllSectors())
        self.wfile.write(sectors.encode('utf-8'))
        return
      params = checkParam('/companies/:sector', self.path)
      if params:
        sector = params[":sector"].replace("%20", " ")
        companies = json.dumps(getBestCompanies(sector))
        self.wfile.write(companies.encode('utf-8'))
        return
      params = checkParam('/company/:cmp', self.path)
      if params:
        sector = params[":cmp"].replace("%20", " ")
        companies = json.dumps(getCompanyDataByAbreviation(sector))
        self.wfile.write(companies.encode('utf-8'))
        return
      self.wfile.write(json.dumps({"Error": "Wrong endpoint!"}).encode('utf-8'))
      return

    def do_POST(self):
      content_length = int(self.headers['Content-Length'])
      post_data = self.rfile.read(content_length)
      logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
              str(self.path), str(self.headers), post_data.decode('utf-8'))
      self._set_response()
      self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info('Starting httpd...\n')
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()