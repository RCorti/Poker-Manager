#!/usr/bin/python
import os, sys, getopt
from lib import config, dbmysql

def help():
    print '\nUsage:\nhh_create_db.py [options]\n\nOptions:\n-n, --name           Create MySQL database \'hh_<name>\'.'
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:", ["name="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-n", "--name"):
            createdb('hh_'+arg)
            
def createdb(dbname):
    TABLES = (
     ("game",  
      "CREATE TABLE `game` ("
      "  `GameID` INT(11) UNSIGNED NOT NULL PRIMARY KEY,"
      "  `Symbol` VARCHAR(1) NOT NULL,"
      "  `Currency` VARCHAR(5) NOT NULL,"
      "  `CreateDate` TIMESTAMP,"
      "  `Button` INT(1) UNSIGNED NOT NULL,"
      "  `Players` INT(1) UNSIGNED NOT NULL,"
      "  `Seats` INT(1) UNSIGNED NOT NULL,"
      "  `AmountSB` FLOAT UNSIGNED NOT NULL,"
      "  `AmountBB` FLOAT UNSIGNED NOT NULL"
      ") ENGINE=InnoDB"
     ),
     
     ("player",
      "CREATE TABLE `player` ("
      "  `PlayerID` INT(4) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
      "  `Name` VARCHAR(50) NOT NULL"
      ") ENGINE=InnoDB"
     ),
     
     ("seat",
      "CREATE TABLE `seat` ("
      "  `GameID` INT(11) UNSIGNED NOT NULL,"
      "  `SeatNo` INT(1) UNSIGNED NOT NULL,"
      "  `PlayerID` INT(4) UNSIGNED NOT NULL,"
      "  `Amount` FLOAT UNSIGNED NOT NULL,"
      "  `StackBB` FLOAT UNSIGNED NOT NULL,"
      "  PRIMARY KEY (`GameID`, `SeatNo`),"
      "  INDEX `IXD_seatPlayer` (`PlayerID` ASC),"
      "  CONSTRAINT `FK_seatGame` FOREIGN KEY (`GameID`) REFERENCES `"+dbname+"`.`game` (`GameID`) ON DELETE CASCADE ON UPDATE RESTRICT,"
      "  CONSTRAINT `FK_seatPlayer` FOREIGN KEY (`PlayerID`) REFERENCES `"+dbname+"`.`player` (`PlayerID`) ON DELETE RESTRICT ON UPDATE RESTRICT"
      ") ENGINE=InnoDB"
     ),

     ("roundlevel",
      "CREATE TABLE `roundlevel` ("
      "  `RoundLevelID` INT(1) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
      "  `Name` VARCHAR(10) NOT NULL"
      ") ENGINE=InnoDB",
      "INSERT INTO `roundlevel` (`Name`) VALUES (%s)",
      [('Preflop',), ('Flop',), ('Turn',), ('River',)]
     ),

     ("betting",
      "CREATE TABLE `betting` ("
      "  `GameID` INT(11) UNSIGNED NOT NULL,"
      "  `RoundLevelID` INT(1) UNSIGNED NOT NULL,"
      "  `Sequence` INT(1) UNSIGNED NOT NULL,"
      "  `SeatNo` INT(1) UNSIGNED NOT NULL,"
      "  `PlayerID` INT(4) UNSIGNED NOT NULL,"
      "  `BetLevel` INT(1) UNSIGNED NOT NULL,"
      "  `AmountPot` FLOAT UNSIGNED NOT NULL,"
      "  `Pot` FLOAT UNSIGNED NOT NULL,"
      "  `Amount` FLOAT UNSIGNED NOT NULL,"
      "  `BB` FLOAT UNSIGNED NOT NULL,"
      "  `BetPot` FLOAT UNSIGNED NOT NULL,"
      "  PRIMARY KEY (`GameID`, `RoundLevelID`, `Sequence`),"
      "  INDEX `IXD_bettingPlayer` (`PlayerID` ASC),"
      "  INDEX `IXD_bettingRoundLevel` (`RoundLevelID` ASC),"
      "  CONSTRAINT `FK_bettingGame` FOREIGN KEY (`GameID`) REFERENCES `"+dbname+"`.`game` (`GameID`) ON DELETE CASCADE ON UPDATE RESTRICT,"
      "  CONSTRAINT `FK_bettingPlayer` FOREIGN KEY (`PlayerID`) REFERENCES `"+dbname+"`.`player` (`PlayerID`) ON DELETE RESTRICT ON UPDATE RESTRICT"
      ") ENGINE=InnoDB"
     ),

     ("queue",
      "CREATE TABLE `queue` ("
      "  `QueueID` INT(16) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
      "  `ActionID` INT(11) UNSIGNED NOT NULL,"
      "  `ValueID` INT(11) UNSIGNED"
      ") ENGINE=InnoDB"
     ),

     ("importgame",
      "CREATE TABLE `importgame` ("
      "  `ImportFileID` INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
      "  `StatusID` INT(11) UNSIGNED,"
      "  `Game` VARCHAR(2048) NOT NULL"
      ") ENGINE=InnoDB"
     )
    )
      
    dbconfig = config.read_config(section='mysql')
    db = dbmysql.db(dbconfig)
    db.create(dbname, TABLES)
    db.close()

if __name__ == '__main__':
    main(sys.argv[1:])