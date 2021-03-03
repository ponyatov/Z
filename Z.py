
import os,sys,re

class Object:
    def __init__(self,V):
        self.value = V
        self.nest = []
    
    def __repr__(self): return self.dump()
    def test(self): return self.dump(test=True)
    def dump(self,cycle=[],depth=0,prefix='',test=False):
        def pad(depth): return '\n'+'\t'*depth
        ret = pad(depth) + self.head(prefix,test)
        return ret
    def head(self,prefix='',test=False):
        hash = f' @{id(self):x}' if not test else ''
        return f'{prefix}<{self.tag()}:{self.val()}>{hash}'
    def tag(self): return f'{self.__class__.__name__.lower()}'
    def val(self): return f'{self.value}'

files = '''
apt.txt
Makefile
requirements.txt
Z.py
.vscode/settings.json
tmp/.gitignore
'''

giti = '''
*
!.gitignore'
'''

class Env(Object): pass

glob = Env('global')

class Web(Object): pass

import flask

class Engine(Web):
    def __init__(self):
        super().__init__('Flask')
        self.app = flask.Flask(self.value)
        self.route()
    def eval(self,env):
        self.app.run(debug=True)
    def route(self):
        @self.app.route('/')
        def index():
            return flask.render_template('index.html',glob=glob)

if __name__ == '__main__':
    Engine().eval(glob)
