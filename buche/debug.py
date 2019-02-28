
from bdb import Bdb
import pdb
import sys


class BucheDb(Bdb):
    __commands__ = [(x.split(':')[0], x.replace(':', '')) for x in [
        's:tep',
        'n:ext',
        'c:ontinue',
        'u:p',
        'd:own'
    ]]

    def __init__(self, repl):
        super().__init__()
        self.repl = repl
        self.frame = None
        self.display_frame = True
        self.stack = []
        self.current = 0

    def eval(self, repl, code, code_globals):
        frame = self.get_frame() # self.stack[self.current]
        gs = {**frame.f_globals, **code_globals.globals}
        ls = frame.f_locals
        lead = code.split(' ')[0]
        for begin, cmd in self.__commands__:
            if lead.startswith(begin) and cmd.startswith(lead):
                self.proceed = getattr(self, f'command_{cmd}')()
                return
        try:
            return eval(code, gs, ls)
        except SyntaxError:
            return exec(code, gs, ls)

    def setup(self, frame, tb):
        self.stack, self.current = self.get_stack(frame, tb)

    def command_step(self):
        self.set_step()
        return True

    def command_next(self):
        self.set_next(self.get_frame())
        return True

    def command_continue(self):
        self.set_continue()
        return True

    def command_up(self):
        self.current = max(self.current - 1, 0)
        self.repl.log(self.get_frame())
        return False

    def command_down(self):
        self.current = min(self.current + 1, len(self.stack) - 1)
        self.repl.log(self.get_frame())
        return False

    def get_frame(self):
        return self.stack[self.current][0]

    def set_frame(self, frame, tb=None):
        self.setup(frame, tb)
        self.repl.log(self.get_frame())
        self.proceed = False
        while not self.proceed:
            self.repl.query(eval=self.eval)

    def user_call(self, frame, args):
        self.repl.log.html('<b>Enter call</b>')
        self.set_frame(frame)

    def user_line(self, frame):
        self.repl.log.html('<b>Next line</b>')
        self.set_frame(frame)

    def user_return(self, frame, rval):
        self.repl.log.html('<b>Return</b>')
        self.set_frame(frame)

    def user_exception(self, frame, exc_info):
        self.repl.log.html('<b>An exception occurred</b>')
        self.repl.log(exc_info)
        self.set_frame(frame)

    def set_trace(self, frame=None):
        self.repl.start(synchronous=True)
        super().set_trace(frame or sys._getframe(1))

    def interaction(self, frame, tb):
        self.repl.start(synchronous=True)
        self.set_frame(frame, tb)
