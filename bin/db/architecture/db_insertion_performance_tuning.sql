#SET SQL_SAFE_UPDATES = 0;           # This allows you drop tables.
#SET foreign_key_checks = 1;         # This drops all foreign key checks.
SET GLOBAL innodb_buffer_pool_size=1073741824‬‬‬;
#show variables like 'innodb_buffer_pool_size%';
#SELECT CEILING(Total_InnoDB_Bytes*1.6/POWER(1024,3)) RIBPS FROM (SELECT SUM(data_length+index_length) Total_InnoDB_Bytes FROM information_schema.tables WHERE engine='InnoDB') A;   # Used to find the maximum memory size.
#SELECT CEILING(SUM(data_length+index_length)/POWER(1024,2)) RIBPS FROM information_schema.tables WHERE engine='InnoDB';

#innodb_buffer_pool_size stats 268435456 (336 mb in Task Mang), 536870912 (582.2 mb in task manager)
#    1073741824 (1145.9 mb in task manager), 1610612736 (1318.6 mb in task manager)