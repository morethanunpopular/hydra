#!/usr/bin/python
from __future__ import print_function
import os
import sys
import time
import requests
import threading
import subprocess
from flask import Flask, jsonify, request

class HydraProcess(object):
  """
  HydraProcess reprsents a Process Hydra manages inside of a container
  """

  def __init__(self, name):
    self.name = name
    self.interface = ProcessInterface(self.name, self.reload, self.healthcheck)

  def run(self, *args):
    self.startThread(self.start, args)
    self.startThread(self.interface.run, [])

  def startThread(self, function, args):
    self.thread = threading.Thread(target=function, args=args, name=self.name)
    self.thread.start()
  
  def healthcheck(self):
    return True

  def reload(self):
    return True

class ProcessInterface(object):
  """
  A ProcessInterface is a simple flask app allowing for remote management of a process managed by Hyrdra
  """
  def __init__(self, name, reload, healthcheck):
    self.app = Flask(name)
    self.process_name = name
    @self.app.route('/{}/healthcheck'.format(self.process_name))
    def health():
      passing = True
      if not healthcheck():
        passing = False
      return jsonify({"passing": passing})
    @self.app.route('/{}/reload'.format(self.process_name), methods=['POST'])
    def reload_endpoint():
      secret = request.headers.get('X-HYDRA-SECRET')
      if secret != HYDRA_SECRET:
        return "authorization required", 403
      if not reload():
        return "failed", 500
      else:
        return "OK", 201
  def run(self):
    self.app.run(port=8080, host='0.0.0.0')

