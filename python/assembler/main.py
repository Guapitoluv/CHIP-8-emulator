import re

rom = """
    SYS 123
"""


class RegexMatch(str):
    """Wrapper to allow regex evaluation inside native match-case blocks."""
    def __eq__(self, pattern: str) -> bool:
        # Uses re.search to find a pattern anywhere in the string.
        # Swap with re.fullmatch if you need to match the entire string.
        return bool(re.search(pattern, self))


def switch(i):
    match RegexMatch(i):
        case r"SYS /\b[0-9a-f]{3}\b/i": return 0x00E0

def assem(rom):
    rom = rom.split(";")
    print(rom)
    a = []
    
    for i, r in enumerate(rom):
        r = r.strip()
        print(r)
        i = len(a)*i
        
        inst = switch(r)
        
        if inst is None: return
        
        a[i] = (inst >> 8) & 0xFF
        a[i+1] = inst & 0xFF
        print(a[i], a[i+1])
assem(rom)