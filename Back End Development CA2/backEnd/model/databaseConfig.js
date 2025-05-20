//Name: Toh Kien Yu
//Class: DAAA/FT/1B/05
//Adm: 2222291

const mysql = require("mysql");
var dbconnect = {
    getConnection: function () {
  
      var conn = mysql.createConnection({
        host: 'localhost',
        port: 3306,
        user: 'bed_dvd_root',
        password: 'pa$$woRD123', //your own password
        database: 'bed_dvd_db',
        dateStrings: true
      });
  
      return conn;
    }
  };
  
module.exports = dbconnect;
  