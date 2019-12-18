# Hydra
Hyrda is a python library meant to be used in the creation of Entrypoint scripts in Docker containers. It provides two useful mechanisms:

* A side-loaded Web App providing healthcheck information
* A remote interface for restarting a managed process

## Quick Example
```
from hydra import HydraProcess 
class nginx(HydraProcess):

  def start(self, *args):
    command = ["nginx"]
    for arg in args:
      command.append(arg)
    self.process = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in iter(self.process.stdout.readline, ''):
      sys.stdout.write(line)

  def reload(self):
    try:
      exit = subprocess.call(["/usr/sbin/nginx", "-s",  "reload"])
      if exit != 0:
        result = False
      else:
        result = True
    except:
      result = False
    return result
    
  def healthcheck(self):
    try:
      r = requests.get('http://localhost')
      if r.status_code != 200:
        return False
      else:
        return True
    except:
      return False

if __name__ == '__main__':
  HYDRA_SECRET = '123'
  proc = nginx('nginx')
  proc.run("-g", "daemon off;")
  while True:
    time.sleep(10)
```

Executing this script will expose a healthcheck endpoint on 8080, and a launch nginx. You could then programtically check the state of the running app thusly:
```
$ curl http://localhost:8080/nginx/healthcheck
{"passing":True}
```
And reload (for example on configuration change) thusly:

```
$ curl -X "POST" http://localhost:8080/nginx/reload -H "X-HYDRA-SECRET: 123"
OK
```

## Features TODO:
* Handle sending signals to the processes

 
