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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Player_Informaiton`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Player_Informaiton` (
  `player_id` VARCHAR(45) NOT NULL,
  `Last_Name` VARCHAR(45) NOT NULL,
  `First_Name` VARCHAR(45) NOT NULL,
  `Player_Debut` DATE NOT NULL,
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`1st_Error_Information_Pitcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`1st_Error_Information_Pitcher` (
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  `Pitcher_Error` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_Event`, `Pitcher_Error`),
  INDEX `Event_First_Err_Pitcher_ID_idx` (`Pitcher_Error` ASC) VISIBLE,
  CONSTRAINT `Event_First_Err`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_First_Err_Pitcher_ID`
    FOREIGN KEY (`Pitcher_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`2nd_Error_Information_Pitcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`2nd_Error_Information_Pitcher` (
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  `Pitcher_Error` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_Event`, `Pitcher_Error`),
  INDEX `Pitcher_Error_2nd_idx` (`Pitcher_Error` ASC) VISIBLE,
  CONSTRAINT `Event_2nd_Error`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Pitcher_Error_2nd`
    FOREIGN KEY (`Pitcher_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`3rd_Error_Information_Pitcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`3rd_Error_Information_Pitcher` (
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  `Pitcher_Error` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_Event`, `Pitcher_Error`),
  INDEX `Pitcher_Id_Three_idx` (`Pitcher_Error` ASC) VISIBLE,
  CONSTRAINT `id_Event_Third_Err`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Pitcher_Id_Three`
    FOREIGN KEY (`Pitcher_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Catcher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Catcher` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `Event_Catch_F_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `Catcher_ID_F`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_Catch_F`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_First_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_First_Base` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `Game_FB_F_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `FB_Foreign_K`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Game_FB_F`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Second_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Second_Base` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_SB_ID`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SB_FK`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Third_Base`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Third_Base` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_TB_ID`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_TB_FK`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Left_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Left_Field` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_LF_ID`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_LF_FK`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Centre_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Centre_Field` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_CF_ID0`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_CF_FK0`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Right_Field`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Right_Field` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_RF_ID0`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_RF_FK0`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Event_Shortstop`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Event_Shortstop` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`player_id`, `event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID0`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK0`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Res_Batter_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Res_Batter_Information` (
  `Res_Batter_ID` VARCHAR(45) NOT NULL,
  `Res_Batter_Hand` VARCHAR(1) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Res_Batter_ID`, `Event_ID`),
  INDEX `Event_ID_Res_FK_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Res_Batter_FK`
    FOREIGN KEY (`Res_Batter_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Res_FK`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Res_Pitcher_Information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Res_Pitcher_Information` (
  `Res_Pitcher_ID` VARCHAR(45) NOT NULL,
  `Res_Pitcher_Hand` VARCHAR(1) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Res_Pitcher_ID`, `Event_ID`),
  INDEX `Event_ID_Res_FK_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Res_Pitcher_FK`
    FOREIGN KEY (`Res_Pitcher_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Res_Pit_FK`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_First_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_First_Details` (
  `Runner_On_First` VARCHAR(45) NOT NULL,
  `Runner_First_Destination` INT NOT NULL,
  `SB_for_runner_on_1st_Flag` VARCHAR(1) NOT NULL,
  `CS_for_runner_on_1st_Flag` VARCHAR(1) NOT NULL,
  `PO_for_runner_on_1st_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_First` VARCHAR(45) NOT NULL,
  `Pitcher_Responsible_For_1st_Runner` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_1st_Flag` VARCHAR(1) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_On_First`, `Pitcher_Responsible_For_1st_Runner`, `Event_ID`),
  INDEX `Runner_1st_Event_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Runner_1st_Event`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_1st_Position`
    FOREIGN KEY (`Runner_On_First`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_1st`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_1st` (
  `Runner_ID` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_ID`, `Event_ID`),
  INDEX `Event_ID_Pinch_1st_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch`
    FOREIGN KEY (`Runner_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_1st`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_Second_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_Second_Details` (
  `Runner_On_Second` VARCHAR(45) NOT NULL,
  `Runner_Second_Destination` INT NOT NULL,
  `SB_for_runner_on_2nd_Flag` VARCHAR(1) NOT NULL,
  `CS_for_runner_on_2nd_Flag` VARCHAR(1) NOT NULL,
  `PO_for_runner_on_2nd_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_Second` VARCHAR(45) NOT NULL,
  `Pitcher_Responsible_For_2nd_Runner` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_2nd_Flag` VARCHAR(1) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_On_Second`, `Pitcher_Responsible_For_2nd_Runner`, `Event_ID`),
  INDEX `Runner_1st_Event_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Runner_2nd_Event`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_2nd_Position`
    FOREIGN KEY (`Runner_On_Second`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_2nd`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_2nd` (
  `Runner_ID` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_ID`, `Event_ID`),
  INDEX `Event_ID_Pinch_1st_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd`
    FOREIGN KEY (`Runner_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Runner_On_Third_Details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Runner_On_Third_Details` (
  `Runner_On_Third` VARCHAR(45) NOT NULL,
  `Runner_Third_Destination` INT NOT NULL,
  `SB_for_runner_on_3rd_Flag` VARCHAR(1) NOT NULL,
  `CS_for_runner_on_3rd_Flag` VARCHAR(1) NOT NULL,
  `PO_for_runner_on_3rd_Flag` VARCHAR(1) NOT NULL,
  `Play_On_Runner_Third` VARCHAR(45) NOT NULL,
  `Pitcher_Responsible_For_3rd_Runner` VARCHAR(45) NOT NULL,
  `Pinch_Runner_On_3rd_Flag` VARCHAR(1) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_On_Third`, `Pitcher_Responsible_For_3rd_Runner`, `Event_ID`),
  INDEX `Runner_1st_Event_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Runner_2nd_Event0`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Runner_2nd_Position0`
    FOREIGN KEY (`Runner_On_Third`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pinch_Runner_Removed_3rd`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pinch_Runner_Removed_3rd` (
  `Runner_ID` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Runner_ID`, `Event_ID`),
  INDEX `Event_ID_Pinch_1st_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd0`
    FOREIGN KEY (`Runner_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd0`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_First_Putout`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_First_Putout` (
  `Fielder_First_Putout` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_First_Putout`, `Event_ID`),
  INDEX `Fielder_Putout_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Putout`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID`
    FOREIGN KEY (`Fielder_First_Putout`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Second_Putout`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Second_Putout` (
  `Fielder_Second_Putout` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Second_Putout`, `Event_ID`),
  INDEX `Fielder_Putout0_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Putout0`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID0`
    FOREIGN KEY (`Fielder_Second_Putout`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Third_Putout`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Third_Putout` (
  `Fielder_Third_Putout` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Third_Putout`, `Event_ID`),
  INDEX `Fielder_Putout00_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Putout00`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID00`
    FOREIGN KEY (`Fielder_Third_Putout`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_First_Assist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_First_Assist` (
  `Fielder_First_Assist` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_First_Assist`, `Event_ID`),
  INDEX `Fielder_First_Putout_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Assist`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Game_Day` (`Game_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Fielder_ID002`
    FOREIGN KEY (`Fielder_First_Assist`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Second_Assist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Second_Assist` (
  `Fielder_Second_Assist` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Second_Assist`, `Event_ID`),
  INDEX `Fielder_Assist0_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Assist0`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID0020`
    FOREIGN KEY (`Fielder_Second_Assist`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Third_Assist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Third_Assist` (
  `Fielder_Third_Assist` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Third_Assist`, `Event_ID`),
  INDEX `Fielder_Assist1_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Assist1`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID0021`
    FOREIGN KEY (`Fielder_Third_Assist`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Fourth_Assist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Fourth_Assist` (
  `Fielder_Fourth_Assist` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Fourth_Assist`, `Event_ID`),
  INDEX `Fielder_Assist2_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Assist2`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID0022`
    FOREIGN KEY (`Fielder_Fourth_Assist`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Fielder_Fifth_Assist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Fielder_Fifth_Assist` (
  `Fielder_Fifth_Assist` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`Fielder_Fifth_Assist`, `Event_ID`),
  INDEX `Fielder_Assist3_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Fielder_Assist3`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fielder_ID0023`
    FOREIGN KEY (`Fielder_Fifth_Assist`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`1st_Error_Information_Positional`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`1st_Error_Information_Positional` (
  `Player_Error` VARCHAR(45) NOT NULL,
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id_Event`, `Player_Error`),
  INDEX `Player_First_Err_idx` (`Player_Error` ASC) VISIBLE,
  CONSTRAINT `Event_First_Err0`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Player_First_Err0`
    FOREIGN KEY (`Player_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`2nd_Error_Information_Positional`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`2nd_Error_Information_Positional` (
  `Player_Error` VARCHAR(45) NOT NULL,
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id_Event`, `Player_Error`),
  INDEX `Player_2nd_Error_idx` (`Player_Error` ASC) VISIBLE,
  CONSTRAINT `Player_2nd_Error0`
    FOREIGN KEY (`Player_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_2nd_Error0`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`3rd_Error_Information_Positional`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`3rd_Error_Information_Positional` (
  `Player_Error` VARCHAR(45) NOT NULL,
  `Error_Type` VARCHAR(5) NOT NULL,
  `id_Event` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id_Event`, `Player_Error`),
  INDEX `Player_2nd_Error_idx` (`Player_Error` ASC) VISIBLE,
  CONSTRAINT `Player_2nd_Error00`
    FOREIGN KEY (`Player_Error`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_2nd_Error00`
    FOREIGN KEY (`id_Event`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Batter_Removed_For_Pinch_Hitter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Batter_Removed_For_Pinch_Hitter` (
  `Runner_ID` VARCHAR(45) NOT NULL,
  `Event_ID` VARCHAR(60) NOT NULL,
  `Position_of_Batter_removed_for_Pinch_Hitter` INT NOT NULL,
  PRIMARY KEY (`Runner_ID`, `Event_ID`),
  INDEX `Event_ID_Pinch_1st_idx` (`Event_ID` ASC) VISIBLE,
  CONSTRAINT `Positional_Player_Pinch_2nd00`
    FOREIGN KEY (`Runner_ID`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Event_ID_Pinch_2nd00`
    FOREIGN KEY (`Event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Batter_In_Event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Batter_In_Event` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  `Batting_Team` INT NOT NULL,
  `Balls` INT NOT NULL,
  `Strikes` INT NOT NULL,
  `Batter_Hand` VARCHAR(1) NOT NULL,
  `Leadoff_Flag` VARCHAR(1) NOT NULL,
  `Pinch_Hit_Flag` VARCHAR(1) NOT NULL,
  `Defensive_Position` INT NOT NULL,
  `Lineup_Position` INT NOT NULL,
  PRIMARY KEY (`event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID00`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK00`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Baseball_Stats_DB`.`Pitcher_In_Event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Baseball_Stats_DB`.`Pitcher_In_Event` (
  `player_id` VARCHAR(45) NOT NULL,
  `event_ID` VARCHAR(60) NOT NULL,
  `Pitcher_Hand` VARCHAR(1) NOT NULL,
  `Pitch_Sequence` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`event_ID`),
  INDEX `game_SB_FK_idx` (`event_ID` ASC) VISIBLE,
  CONSTRAINT `player_SS_ID000`
    FOREIGN KEY (`player_id`)
    REFERENCES `Baseball_Stats_DB`.`Player_Informaiton` (`player_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `game_SS_FK000`
    FOREIGN KEY (`event_ID`)
    REFERENCES `Baseball_Stats_DB`.`Event_Instance` (`idEvent`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
