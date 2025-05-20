//Name: Toh Kien Yu
//Class: DAAA/FT/1B/05
//Adm: 2222291
var app = require("./controller/app");
var port = 3036;
var server = app.listen(port, () => {

    console.log(`Web App Hosted at http://localhost:${port}`);

});