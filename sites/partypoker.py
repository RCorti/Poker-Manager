import re
from lib import config, dbmysql

class HH_ParseError(Exception):
    def __init__(self, arg):
        self.args = arg
    def __str__(self):
        return repr(self.args)

def isValid(part):
    return not (None == re.match('\*{5}\s.*', part))

def parse(body):
    def valNone(pattern, line):
        return None == re.match(pattern, line)
    
    def test(pattern, line):
        return not valNone(pattern, line)
        
    def match(pattern, line):
        result = re.match(pattern, line)
        if result == None:
            raise HH_ParseError("PartyPoker pattern error: {} -> {}".format(pattern, line))
        return result.groups()
        
    def CheckLine(patterns, line):
        for index, pattern in patterns:
            result = re.match(pattern, line)
            if not (result == None):
                return (index, result.groups())
        print "PartyPoker: Miss pattern for line: {}".format(line)        
        raise HH_ParseError("")
        
        
    try:
        lines = body.splitlines()
    
        GameId, = match('.*\sGame\s(\d+)', lines[0])
        GameType, GameDate = match('(.*)\s-\s(.*)', lines[1])
        TableName, = match('Table\s(.*)', lines[2])
        ButtonSeat, = match('Seat\s(\d+)\s.*button', lines[3])
        ButtonSeat = int(ButtonSeat)
        NoOfPlayers, NoOfSeats = match('.*\splayers.*(\d+)/(\d+)', lines[4])
        NoOfPlayers = int(NoOfPlayers)
        NoOfSeats = int(NoOfSeats)
        SeatNoPlayer = [''] * NoOfSeats
        PlayerSeat = {}
        PlayerAmount = {}
        for lineno in range(5, 5 + int(NoOfPlayers)):
            line = lines[lineno]
            _seatno, _name, _stack = match('Seat\s(\d+):\s(.*)\s\(\s*.([\d.]+)', line)
            _seatno = int(_seatno)
            _stack = float(_stack)
            SeatNoPlayer[_seatno-1] = _name
            PlayerSeat[_name] = _seatno
            PlayerAmount[_name] = _stack
        
        patterns = (
            (  1, '^(\S+) folds' ),
            (  2, '^(\S+) raises \[.([\d.]+)' ),
            (  3, '^(\S+) wins .([\d.]+)' ),
            (  4, '^(\S+) calls \[.([\d.]+)' ),
            (  5, '^(\S+) bets \[.([\d.]+)' ),
            (  6, '^(\S+) checks' ),
            (  7, '^\*\* Dealing Flop \*\*.*\[ *(\S\S), *(\S\S), *(\S\S)' ),
            (  8, '^\*\* Dealing Turn \*\*.*\[ *(\S\S)' ),
            (  9, '^\*\* Dealing River \*\*.*\[ *(\S\S)' ),
            ( 10, '\*\* (Dealing) down cards \*\*' ),
            ( 11, '^(\S+) posts (\S+) blind.*\[.([\d.]+)'),
            ( 12, '^Dealt to (\S+) \[ *(\S+) (\S+)' ),
            ( 13, '^(\S+) is all-In *\[.([\d.]+)' ),
            ( 14, '^(\S+) did not respond in time' ),
            ( 15, '^(\S+) shows \[ (\S\S), (\S\S)' ),
            ( 16, '^(\S+) doesn.t show \[ (\S\S), (\S\S)' ),
            ( 17, '^(\S+) does not show' ),
            ( 18, '^(\S+) is sitting out' ),
            ( 19, '^(\S+) could not respond in time' ),
            ( 20, '^(\S+) has been reconnected' ),
            ( 21, '^(\S+): (.*)$' ), # chat
            ( 22, '^(\S+) .*time bank' ),
            ( 23, '^(\S+) has left' ),
            ( 24, '^(\S+) has joined' )
        )
        
        level = -1
        turn = -1
        for lineno in range(5 + int(NoOfPlayers), len(lines)):
            line = lines[lineno]
            index, results = CheckLine(patterns, line)
            if index == 1:
                #player: chat
                results = None
            elif index == 2:
                #** Dealing down cards **
                results = None
          

    except HH_ParseError:
        print "_______________"
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
       
