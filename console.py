import datetime
from _io import TextIOWrapper
from collections import deque
from lark import UnexpectedInput,UnexpectedCharacters,UnexpectedToken
import curses
from lark import Lark,Tree,Transformer

class ConsoleTransformer(Transformer):
    def __init__(self,console,*args):
        Transformer.__init__(self,*args)
        self.console=console
        self.history=self.console.history
        self.ps1 = self.console.ps1
        self.ps2 = self.console.ps2

    def buffer(self,args):
        n = args[1]
        if n is None : n = 1
        else : n= int(n)
        
        if n<=0: n = 1

        n= min(n,len(self.history))
        for i in range(n):
            m = len(self.history)-i-1
            command = self.history[m]
            command = command.replace("\n","\n    ")
            print("{})  {}".format(i+1,command))

    def load(self,args):
        n = args[1]
        if n is None : n = 1
        else : n= int(n)
        
        if n<=0: n = 1

        if n>=len(self.history):
            print("no command number {} on history".format(n))

        else :
            command = self.history[-n]
            command = command.replace("\n","\n    ")
            print("processing : \n    {}".format(command))
            self.console.handle_command(command)

        






class Console:
    separator = "__CONSOLE_LINE_OUT_24343243__\n"
    ps_state = 1
    root = None
    height = 0
    width = 0
    window = None
    w_height = 0
    w_width = 0
    upper_x = 0
    upper_y = 0
    cursor_x = 0
    cursor_y = 0

    def __init__(self,parser,init_msg=None,max_line_break=1,ps1=None,ps2=None,history=None,max_history=1000,history_out=None):
        """
            parser = takes a str and return str
            init_msg = shows at init
            max_line_breack = max line break allowed on stream before take input and parse
            ps1 = principal console line
            ps2 = shows after linebreak without max_line_break
        """
        self.parser = parser

        if init_msg and (isinstance(init_msg,str)):
            self.init_msg = init_msg
        else : self.init_msg = "Default console start ({})".format(datetime.datetime.now())

        self.max_line_break = max(max_line_break,0)

        self.config_ps(ps1,ps2)

        self.config_history(history,max_history,history_out)

        with open("console_grammar.lk","r") as console_grammar:
            self.console_parser = Lark(console_grammar, parser='lalr', start = "command",
                                    maybe_placeholders=True)

        self.console_transformer = ConsoleTransformer(self)

    def config_ps(self,ps1,ps2):
        if ps1 and (isinstance(ps1,str)) : 
            self.ps1 = ps1
        else : self.ps1 = "✿ > "

        if ps2 and (isinstance(ps2,str)) : 
            self.ps2 = ps2
        else : self.ps2 = ""


    def config_history(self,history,max_history,history_out):
        self.max_history=max_history

        if history :
            if isinstance(history,TextIOWrapper):
                self.history = deque(self.read_history(history),self.max_history)
            elif isinstance(history,str):
                #TODO check if file exist
                with open(history,"r") as h_file :
                    self.history = deque(self.read_history(h_file),self.max_history)
        else : 
            self.history = deque([],self.max_history)

        if history_out:
            self.history_out = history_out
        else :
            self.history_out = ".__CONSOLE_HISTORY__21312323"


    def read_history(self,file_obj):
        lines_acc = []
        for line in file_obj:
            if line != self.separator:
                lines_acc.append(line)
            else : 
                out= "".join(lines_acc)
                lines_acc=[]
                yield(out)

    def add_to_history(self,command):
        self.history.append(command)

    def write_history(self):
        with open(self.history_out,"w") as out:
            for command in self.history:
                out.write(command)
                out.write(self.separator)

    # def start(self):
    #     curses.wrapper(self.start_)

    # def start_(self,stdscr):
    #     self.root = stdscr
    #     self.height,self.width = self.root.getmaxyx()
    #     self.configure_pad()
    #     try : 
    #         self.cycles()
    #     except KeyboardInterrupt:
    #         self.close()
    #     except EOFError :
    #         self.close()

    # def cycles(self):
    #     while(True):
    #         c=self.window.getkey()
    #         self.draw_text(c)

    #     # c = pad.getch(2,3)
    #     # self.handle_keys(c)
    #     # pad.addstr(str(c))
    #     # pad.refresh(0,0,0,0,12,40)
    #     # pad.getkey()

    # def configure_pad(self):    
    #     self.w_height = 1000
    #     self.w_width = 200
    #     self.window= curses.newpad(self.w_height, self.w_width)


    # def cycle(self,key):
    #     if key == curses.KEY_RESIZE:
    #         self.on_resize()
    #     elif key == curses.KEY_UP:




    # def draw_text(self,text):
    #     self.cursor_y+=1
    #     self.window.addstr(self.cursor_y,self.cursor_x,text)
    #     self.window.refresh(self.cursor_y,self.upper_x,0,0,self.height-1,self.width-1)

    # def 

    # def on_resize(self):
    #     self.height,self.width = self.root.getmaxyx()


    def start(self):
        self.write(self.init_msg,show_ps=False)
        try:
            self.cycles()
        except KeyboardInterrupt:
            self.close()
        except EOFError:
            self.close()

    def cycle(self):
        break_counter=0
        in_str = [input(self.ps1)]

        if in_str == '' : break_counter+=1

        while(break_counter<self.max_line_break) :
            in_str.append(input(self.ps2))
            if in_str[-1]=='' : break_counter+=1
            else : break_counter=0

        command = "".join(in_str)
        if command :
            if command.startswith(":"):
                self.handle_console_command(command)
                return
            self.handle_command(command)

    def handle_command(self,command):
        self.add_to_history(command+"\n")
        try:
            out = self.parser.parse(command)
        except UnexpectedCharacters as u : 
            self.char_exception(u,command)
            return 
        except UnexpectedToken as u : 
            self.token_exception(u,command)
            return 
        for tree in out:
            self.write(tree,show_ps=False)

    def handle_console_command(self,command):
        try:
            tree = self.console_parser.parse(command)
        except UnexpectedInput as u:
            self.write_error(str(u))
            return 
        self.console_transformer.transform(tree)


    def cycles(self):
        while(True):
            self.cycle()

    def close(self):
        self.write_history()

    def write(self,content,show_ps=True):
        if show_ps:
            print(self.ps1,end="")
        print(content)

    def write_error(self,error):
        print(error)

    def char_exception(self,error,command):
        self.write_error(str(error))

    def token_exception(self,error,command):
        col = error.column
        section = command[:col]
        msg = "{}\n{}\n{}".format(section,((col+1)*" ")+"^",str(error))
        self.write_error(msg)

    def console_exception(self):
        print("CONSOLE_ERROR")


