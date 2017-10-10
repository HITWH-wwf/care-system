import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/common")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tornado.ioloop
import tornado.web
import tornado.httpserver
import traceback
import views
import urls
import subprocess
import time
from multiprocessing import Manager, freeze_support

port = 8006

def main(first, app, num = 1):
    if str(first) == 'duo':
        freeze_support()
        print ("duo")
        print ("Quit the server with CONTROL-C.")
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.bind(port)
        http_server.start(num_processes = num) # tornado将按照cpu核数来fork进程
        tornado.ioloop.IOLoop.instance().start()
    elif str(first) == 'dan':
        app.listen(port)
        print ("dan")
        print ("Starting development server at http://127.0.0.1:" + str(port) )
        print ("Quit the server with CONTROL-C.")
        tornado.ioloop.IOLoop.instance().start()
    else:
        pass

def kill_port_used(port):
    """kill掉占用该端口的进程，确保程序可以正常启动"""
    try:
        ans = subprocess.Popen(["lsof","-i",":%d"%int(port)], shell=False, stdout = subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
        ans = str(ans, encoding = "UTF-8")  
        ans = ans.splitlines()
        pid_set = set()
        for con in ans:
            if "(LISTEN)" in con:
                pid_set.add(con.split(" ")[2])
        if len(pid_set) == 0:
            return None
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ini/kill_port_%d.txt"%int(port)), "w") as f:
            f.write("\n".join(list(pid_set)))
        os.system("cat %s | xargs kill -9"%os.path.join(os.path.dirname(os.path.abspath(__file__)), "ini/kill_port_%d.txt"%int(port)))
    except:
        error_info = traceback.format_exc()
        print (error_info)

if __name__ == "__main__":
    app = urls.application
    global port
    #kill_port_used(port)
    try:
        main("dan", app)
        #main("duo", app, 10)
    except:
        kill_port_used(port)
        time.sleep(1)
        error_info = traceback.format_exc()
        print (error_info)
        main("dan", app)
