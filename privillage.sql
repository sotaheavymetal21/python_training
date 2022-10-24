CREATE USER IF NOT EXISTS 'aiful'@'%' IDENTIFIED BY 'AEW/zq_rr+c6';
GRANT USAGE ON *.* TO 'aiful'@'%';
GRANT CREATE, DROP ON 'pc_app_form'.* TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'customer' TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'basic_information' TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'residence_adderss' TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'residence_information' TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'employment' TO 'aiful'@'%';
GRANT SELECT, CREATE, REFERENCES ON 'pc_app_form'.'workplace' TO 'aiful'@'%';
FLUSH PRIVILEGES;

grant type_of_permission on database_name.table_name to ユーザ名@ホスト名;

grant create on 'pc_app_form'.* to 'aiful'@'%';
grant drop on 'pc_app_form'.* to 'aiful'@'%';
rirekigahukugennsaremasita. kanaruhodon enone check yu-zamei hosutomei table name pribileges type of poermission create
