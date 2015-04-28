# -*- coding: utf-8 -*- 
import torndb
from urllib import urlencode
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys,os
import tornado.autoreload
import tornado.gen 
import time
import MySQLdb,functools,urlparse
from tornado.options import define, options, parse_command_line
reload(sys)
sys.setdefaultencoding('utf8')

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="account database host")
define("mysql_database", default="account", help="account database name")
define("mysql_user", default="root", help="account database user")
define("mysql_password", default="", help="account database password")


class Application(tornado.web.Application):
    def __init__(self):
	settings = {                                                              
     "static_path": os.path.join(os.path.dirname(__file__), "../static"),                         
     "template_path" : os.path.join(os.path.dirname(__file__), "../template"),                    
     "login_url": "/login/",                                                 
     "debug" : True,                                                      
     "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",                          
	#"xsrf_cookies":True,                                                  
	}                                                                   
                                                                    
	handlers =[                                                
    		(r"/", user),                                                       
    		(r"/out/", loginout),                                                    
    		(r"/user/", user),                                                       
    		(r"/login/", login),                                                     
    		(r"/useradd/", useradd),                                                
    		(r"/userdel/", userdel),                                                
     ]                                                             

     	tornado.web.Application.__init__(self, handlers, **settings)
	try:
         self.db = torndb.Connection(                                               
        	host=options.mysql_host, database=options.mysql_database,                             
         	user=options.mysql_user, password=options.mysql_password,charset='utf8')
	except:
	    print  "数据库连接不上"
#####################################                                         
#权限说明：
# 1管理员
# 2用户
# 3运维
# 4研发
# 5厂家
###############################
#admin管理员权限
def is_admin(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
     if not self.current_user :
         if self.request.method in ("GET", "HEAD"):
          url = self.get_login_url()
          if "?" not in url:
              if urlparse.urlsplit(url).scheme:
               next_url = self.request.full_url()
              else:
               next_url = self.request.uri
              url += "?" + urlencode(dict(next=next_url))
          self.redirect(url)
          return
         raise tornado.web.HTTPError(403)
     """
     else:
	    role_ID=self.db.get("SELECT role FROM user WHERE user = %s ", self.current_user) 
	    if int(role_ID['role']) != 4:
	     	self.write("您没有权限,页面即将跳转 ")
	     	return
     """

     return method(self, *args, **kwargs)
    return wrapper

#####################################                                         


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
     return self.application.db
    def get_current_user(self):
     return self.get_secure_cookie("user")

class user(BaseHandler):
    @is_admin
    def get(self):
	department = self.db.get("SELECT sele ,role FROM user WHERE user = %s", self.current_user)
	print department['role']
	if int(department['role']) == 4:
		users=self.db.query("SELECT * FROM user")
	else:
		users=self.db.query("SELECT * FROM user where sele='%s '" %(department['sele']))
     	self.render("user.html",users = users,department=department['sele'])
class loginout(BaseHandler):
    def get(self):
	self.set_secure_cookie("user"," ")
     	self.clear_cookie("user")
     	self.redirect('/login/', permanent=True)
class login(BaseHandler):
    def get(self):
     self.render("login.html")
    def post(self):
	name		=self.get_argument("name")
	pd		=self.get_argument("passwd")
	results = self.db.get("SELECT user , passwd ,sele FROM user WHERE user = %s", name)
	if results:
    	    if  results['passwd'] == pd :
    		self.set_secure_cookie("user", name)
    		self.redirect('/user/', permanent=True)
    		
    	    else:
    		self.write("密码不对")
	else:
    	    self.write("没有这个用户")


class useradd(BaseHandler):
    def post(self):
     user  	=self.get_argument("user")
     passwd	=self.get_argument("passwd")
     email  	= self.get_argument("email")
     tel	= self.get_argument("tel")
     sele 	= self.get_argument("sele")
     role	=self.get_argument("role")
     print    self.get_argument("priv")
     last_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
     sql 	= "INSERT INTO user(user,passwd,email, tel, sele,role,last_time) VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(user,passwd,email,tel,sele,role,last_time)
     self.db.execute(sql)
class userdel(BaseHandler):                                                                                         
    def post(self):                                                                                                 
      account 	=self.get_argument("account") 
      deparment	= self.get_argument("deparment") 
      sql	="delete  user from user where user='%s' and sele='%s'"%(account,deparment)
      self.db.execute(sql)


def main():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
