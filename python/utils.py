from pathlib import Path
import inspect

class Logger:
    def __init__(self) -> None:
        self.logs = {}
        self.last_log = None

    def log(self, *args):
        frame = inspect.currentframe().f_back
    
        file = Path(frame.f_code.co_filename)
        filepath = ".../" + file.parent.name + "/" + file.name
        linha = frame.f_lineno
        
        log = f"[ {filepath}, line {linha} ] " + " ".join(args)
        
        if log in self.logs.keys():
            self.logs[log]["now"] += 1
        else:
            self.logs[log] = {"total": 0, "now": 1}
        
        if self.last_log != log:
            if self.last_log is not None:
                self.logs[self.last_log]["total"] += self.logs[self.last_log]["now"]
                print(self.last_log.replace("]", f"({self.logs[self.last_log]["total"]}-{self.logs[self.last_log]["now"]}) ]"), end="\n\n")
                self.logs[self.last_log]["now"] = 0
            
            self.last_log = log