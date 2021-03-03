
import os,sys,re
import datetime as dt

class Object:
    def __init__(self,V):
        self.value = V
        self.slot = {}
        self.nest = []
    
    def __repr__(self): return self.dump()
    def test(self): return self.dump(test=True)
    def dump(self,cycle=[],depth=0,prefix='',test=False):
        def pad(depth): return '\n'+'\t'*depth
        # head
        ret = pad(depth) + self.head(prefix,test)
        # cycle
        if not depth: cycle=[]
        if self in cycle: return ret + ' _/'
        else: cycle.append(self)
        # slot{}s
        for i in self.keys():
            ret += self[i].dump(cycle,depth+1,f'{i} = ',test)
        # nest[]ed
        # sutree
        return ret
    def head(self,prefix='',test=False):
        hash = f' @{id(self):x}' if not test else ''
        return f'{prefix}<{self.tag()}:{self.val()}>{hash}'
    def tag(self): return f'{self.__class__.__name__.lower()}'
    def val(self): return f'{self.value}'

    def keys(self):
        return sorted(self.slot.keys())
    def __getitem__(self,key):
        assert isinstance(key,str)
        return self.slot[key]
    def __setitem__(self,key,that):
        assert isinstance(key,str)
        assert isinstance(that,Object)
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        return self.__setitem__(that.tag(),that)
    def __rshift__(self,that):
        return self.__setitem__(that.val(),that)

    def html(self): return self.head()

class Env(Object): pass

glob = Env('global')

class IO(Object): pass

class Time(IO):
    def __init__(self,V=None):
        if not V:
            self.now = dt.datetime.now()
            self.date = self.now.strftime('%Y-%m-%d')
            self.time = self.now.strftime('%H:%M:%S')
            V = f'{self.now}'
        super().__init__(V)
    def json(self):
        return {"date":self.date,"time":self.time}

class Meta(Object): pass

meta = Meta('info') ; glob << meta

class Module(Meta): pass

meta['MODULE'] = MODULE = Module('metaL')

class Title(Meta):
    def html(self):
        return f'<i>{self.value}</i>'

meta['TITLE'] = TITLE = Title('object graph database + web platform')

class Author(Meta):
    def html(self):
        email = f' {self["email"].html()}' if 'email' in self.keys() else ''
        return f'{self.val()}{email}'

meta['AUTHOR'] = AUTHOR = Author('Dmitry Ponyatov')

class Web(Object): pass

class EMail(Web):
    def html(self):
        return f'&lt;<a href="mailto:{self.value}">{self.value}</a>&gt;'

meta['EMAIL'] = EMAIL = EMail('dponyatov@gmail.com')
AUTHOR << EMAIL

class Url(Web):
    def html(self):
        return f'<a href="{self.value}">{self.value}</a>'

meta['GITHUB'] = Url('https://github.com/ponyatov/Z')

import flask
from flask_socketio import SocketIO


class Engine(Web):
    def __init__(self):
        super().__init__('Flask')
        self.app = flask.Flask(self.value)
        self.route()
        self.sio = SocketIO(self.app)
        self.socket()
    def eval(self,env):
        self.sio.run(self.app,debug=True)
    def route(self):
        @self.app.route('/')
        def index():
            return flask.render_template('index.html',glob=glob,env=glob)
    def socket(self):
        @self.sio.on('connect')
        def connect(): self.sio.emit('localtime',Time().json())

if __name__ == '__main__':
    Engine().eval(glob)
