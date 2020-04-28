-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Baseball_Stats_DB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Baseball_Stats_DB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Baseball_Stats_DB` DEFAULT CHARACTER SET utf8 ;
USE `Baseball_Stats_DB` ;

-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Game_Day`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Game_Day` (
  `Visiting_Team` VARCHAR(45) NOT NULL,
  `Home_Team` VARCHAR(45) NOT NULL,
  `Game_ID` VARCHAR(45) NOT NULL,
  `Date` VARCHAR(45) NOT NULL,
  `NumGameInDay` INT NOT NULL,
  PRIMARY KEY (`Game_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Instance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Instance` (
  `idEvent` VARCHAR(60) NOT NULL,
  `Game_ID` VARCHAR(45) NOT NULL,
  `Inning` INT UNSIGNED NOT NULL,
  `Outs` INT UNSIGNED NOT NULL,
  `Vis_Score` INT NOT NULL,
  `Home_Score` INT NOT NULL,
  `Event_Text` VARCHAR(45) NOT NULL,
  `Event_Type` INT NOT NULL,
  `Batter_Event_Flag` VARCHAR(1) NOT NULL,
  `AB_Flag` VARCHAR(1) NOT NULL,
  `Hit_Value` INT NOT NULL,
  `SH_Flag` VARCHAR(1) NOT NULL,
  `SF_Flag` VARCHAR(1) NOT NULL,
  `Outs_on_Play` INT NOT NULL,
  `Double_Play_Flag` VARCHAR(1) NOT NULL,
  `Triple_Play_Flag` VARCHAR(1) NOT NULL,
  `RBI_On_Play` INT NOT NULL,
  `Wild_Pitch_Flag` VARCHAR(1) NOT NULL,
  `Passed_Ball_Flag` VARCHAR(1) NOT NULL,
  `Fielded_By` INT NOT NULL,
  `Batted_Ball_Type` VARCHAR(45) NOT NULL,
  `Bunt_Flag` VARCHAR(1) NOT NULL,
  `Foul_Flag` VARCHAR(1) NOT NULL,
  `Hit_Location` VARCHAR(45) NOT NULL,
  `Num_Errors` INT NOT NULL,
  `Batter_Dest` INT NOT NULL,
  `Play_on_Batter` VARCHAR(45) NOT NULL,
  `New_Game_Flag` VARCHAR(1) NOT NULL,
  `End_Game_Flag` VARCHAR(1) NOT NULL,
  PRIMARY KEY (`idEvent`),
  INDEX `Game_ID_idx` (`Game_ID` ASC) VISIBLE,
  CONSTRAINT `Game_ID`
    FOREIGN KEY (`Game_ID`)
    REFERENCES `Baseball_Stats_DB`.`Game_Day` (`Game_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Player_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Player_Information` (
  `player_id` VARCHAR(45) NOT NULL,
  `Last_Name` VARCHAR(45) NOT NULL,
  `First_Name` VARCHAR(45) NOT NULL,
  `Player_Debut` DATE NOT NULL,
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Catcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Catcher` (
  `Catcher` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Catcher`, `idEvent`),
  INDEX `Event_Catch_F_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Catcher_ID_F`
    FOREIGN KEY (`Catcher`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_Catch_F`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_First_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_First_Base` (
  `First_Base` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`First_Base`, `idEvent`),
  INDEX `Game_FB_F_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `FB_Foreign_K`
    FOREIGN KEY (`First_Base`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Game_FB_F`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Second_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Second_Base` (
  `Second_Base` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Second_Base`, `idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_SB_ID`
    FOREIGN KEY (`Second_Base`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SB_FK`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Third_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Third_Base` (
  `Third_Base` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Third_Base`, `idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_TB_ID`
    FOREIGN KEY (`Third_Base`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_TB_FK`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Left_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Left_Field` (
  `Left_Field` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Left_Field`, `idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_LF_ID`
    FOREIGN KEY (`Left_Field`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_LF_FK`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Centre_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Centre_Field` (
  `Center_Field` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Center_Field`, `idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_CF_ID0`
    FOREIGN KEY (`Center_Field`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_CF_FK0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Right_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Right_Field` (
  `Right_Field` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Right_Field`, `idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_RF_ID0`
    FOREIGN KEY (`Right_Field`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_RF_FK0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Shortstop`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Shortstop` (
  `idEvent` VARCHAR(60) NOT NULL,
  `Shortstop` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEvent`, `Shortstop`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID0`
    FOREIGN KEY (`Shortstop`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Res_Batter_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Res_Batter_Information` (
  `Res_Batter_Name` VARCHAR(45) NOT NULL,
  `Res_Batter_Hand` VARCHAR(1) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Res_Batter_Name`, `idEvent`),
  INDEX `Event_ID_Res_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Res_Batter_FK`
    FOREIGN KEY (`Res_Batter_Name`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Res_FK`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Res_Pitcher_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Res_Pitcher_Information` (
  `Res_Pitcher_Name` VARCHAR(45) NOT NULL,
  `Res_Pitcher_Hand` VARCHAR(1) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Res_Pitcher_Name`, `idEvent`),
  INDEX `Event_ID_Res_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Res_Pitcher_FK`
    FOREIGN KEY (`Res_Pitcher_Name`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Res_Pit_FK`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_First_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_First_Details` (
  `First_Runner` VARCHAR(45) NOT NULL,
  `Runner_On_1st_Dest` INT NOT NULL,
  `SB_Runner_On_1st_Flag` VARCHAR(1) NOT NULL,
  `CS_Runner_On_1st_Flag` VARCHAR(1) NOT NULL,
  `PO_For_Runner_On_1st_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_On_1st` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_1st` VARCHAR(1) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`First_Runner`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_1st_Position`
    FOREIGN KEY (`First_Runner`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_1st`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_1st` (
  `Runner_Removed_For_Pinch_Runner_On_1st` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_Removed_For_Pinch_Runner_On_1st`, `idEvent`),
  INDEX `Event_ID_Pinch_1st_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch`
    FOREIGN KEY (`Runner_Removed_For_Pinch_Runner_On_1st`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_1st`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_2nd`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_2nd` (
  `Runner_Removed_For_Pinch_Runner_On_2nd` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_Removed_For_Pinch_Runner_On_2nd`, `idEvent`),
  INDEX `Event_ID_Pinch_1st_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd`
    FOREIGN KEY (`Runner_Removed_For_Pinch_Runner_On_2nd`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_3rd`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_3rd` (
  `Runner_Removed_For_Pinch_Runner_On_3rd` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_Removed_For_Pinch_Runner_On_3rd`, `idEvent`),
  INDEX `Event_ID_Pinch_1st_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd0`
    FOREIGN KEY (`Runner_Removed_For_Pinch_Runner_On_3rd`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Assist_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Assist_Information` (
  `idEvent` VARCHAR(60) NOT NULL,
  `Fielder_Number` INT NOT NULL,
  `Assist_Number` INT NOT NULL,
  PRIMARY KEY (`idEvent`, `Assist_Number`),
  CONSTRAINT `Fielder_Assist`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Error_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Error_Information` (
  `Error_Player` INT NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  `Error_Type` VARCHAR(1) NOT NULL,
  `Error_Position` INT NOT NULL,
  PRIMARY KEY (`idEvent`, `Error_Position`),
  CONSTRAINT `Event_First_Err0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Batter_Removed_For_Pinch_Hitter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Batter_Removed_For_Pinch_Hitter` (
  `Batter_Removed_For_Pinch_Hitter` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  `Position_of_Batter_removed_for_Pinch_Hitter` INT NOT NULL,
  PRIMARY KEY (`Batter_Removed_For_Pinch_Hitter`, `idEvent`),
  INDEX `Event_ID_Pinch_1st_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd00`
    FOREIGN KEY (`Batter_Removed_For_Pinch_Hitter`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd00`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Batter_In_Event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Batter_In_Event` (
  `Batter_Name` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  `Batting_Team` INT NOT NULL,
  `Balls` INT NOT NULL,
  `Strikes` INT NOT NULL,
  `Batter_Hand` VARCHAR(1) NOT NULL,
  `Leadoff_Flag` VARCHAR(1) NOT NULL,
  `Pinch_Hit_Flag` VARCHAR(1) NOT NULL,
  `Defensive_Position` INT NOT NULL,
  `Lineup_Position` INT NOT NULL,
  PRIMARY KEY (`idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID00`
    FOREIGN KEY (`Batter_Name`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK00`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pitcher_In_Event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pitcher_In_Event` (
  `Pitcher_Name` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  `Pitcher_Hand` VARCHAR(1) NOT NULL,
  `Pitch_Sequence` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEvent`),
  INDEX `game_SB_FK_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID000`
    FOREIGN KEY (`Pitcher_Name`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK000`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Responsible_Pitcher_For_First`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Responsible_Pitcher_For_First` (
  `Responsible_Pitcher_For_Runner_On_1st` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Responsible_Pitcher_For_Runner_On_1st`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Responsible_Pitcher_One`
    FOREIGN KEY (`Responsible_Pitcher_For_Runner_On_1st`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Responsible_Pitcher_For_Second`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Responsible_Pitcher_For_Second` (
  `Responsible_Pitcher_For_Runner_On_2nd` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Responsible_Pitcher_For_Runner_On_2nd`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event00`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Resp_Pitcher_Two`
    FOREIGN KEY (`Responsible_Pitcher_For_Runner_On_2nd`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Responsible_Pitcher_For_Third`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Responsible_Pitcher_For_Third` (
  `Responsible_Pitcher_For_Runner_On_3rd` VARCHAR(45) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Responsible_Pitcher_For_Runner_On_3rd`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event000`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Resp_Pitcher_Third`
    FOREIGN KEY (`Responsible_Pitcher_For_Runner_On_3rd`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_Second_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_Second_Details` (
  `Second_Runner` VARCHAR(45) NOT NULL,
  `Runner_On_2nd_Dest` INT NOT NULL,
  `SB_Runner_On_2nd_Flag` VARCHAR(1) NOT NULL,
  `CS_Runner_On_2nd_Flag` VARCHAR(1) NOT NULL,
  `PO_For_Runner_On_2nd_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_On_2nd` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_2nd` VARCHAR(1) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Second_Runner`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event1`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_1st_Position0`
    FOREIGN KEY (`Second_Runner`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_Third_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_Third_Details` (
  `Third_Runner` VARCHAR(45) NOT NULL,
  `Runner_On_3rd_Dest` INT NOT NULL,
  `SB_Runner_On_3rd_Flag` VARCHAR(1) NOT NULL,
  `CS_Runner_On_3rd_Flag` VARCHAR(1) NOT NULL,
  `PO_For_Runner_On_3rd_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_On_3rd` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_3rd` VARCHAR(1) NOT NULL,
  `idEvent` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Third_Runner`, `idEvent`),
  INDEX `Runner_1st_Event_idx` (`idEvent` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event10`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_1st_Position00`
    FOREIGN KEY (`Third_Runner`)
    REFERENCES `Baseball_Stats_DB`.`Player_Information` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Putout_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Putout_Information` (
  `idEvent` VARCHAR(60) NOT NULL,
  `Fielder_Number` INT NOT NULL,
  `Putout_Number` INT NOT NULL,
  PRIMARY KEY (`idEvent`, `Putout_Number`),
  CONSTRAINT `Fielder_Assist0`
    FOREIGN KEY (`idEvent`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
