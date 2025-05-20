//Name: Toh Kien Yu
//Class: DAAA/FT/1B/05
//Adm: 2222291

const express=require('express');
const serveStatic=require('serve-static');

var hostname="localhost";
var port=3001;

var app=express();

app.use(function(req,res,next){
    console.log(req.url);
    console.log(req.method);
    console.log(req.path);
    console.log(req.query.id);
    if(req.method!="GET"){
        res.type('.html');
        var msg="<html><body>This server only serves web pages with GET!</body></html>";
        res.end(msg);
    }else{
        next();
    }
});

app.get("/login/", (req, res) => {
    res.sendFile("/public/login.html", { root: __dirname });
});

app.get("/", (req, res) => {
    res.sendFile("/public/viewFilms.html", { root: __dirname });
});

app.get("/viewFilms", (req, res) => {
    res.sendFile("/public/viewFilms.html", { root: __dirname });
});

app.get("/addCustomer", (req, res) => {
    res.sendFile("/public/addCustomer.html", { root: __dirname });
});

app.get("/addActor", (req, res) => {
    res.sendFile("/public/addActor.html", { root: __dirname });
});

app.get("/cart", (req, res) => {8
    res.sendFile("/public/cart.html", { root: __dirname });
});

app.get("/deleteActor", (req, res) => {
    res.sendFile("/public/deleteActor.html", { root: __dirname });
});


app.get("/checkout", (req, res) => {
    res.sendFile("/public/checkout.html", { root: __dirname });
});

app.get("/review", (req, res) => {
    res.sendFile("/public/review.html", { root: __dirname });
});


app.use(serveStatic(__dirname+"/public"));

// app.get("/login/", (req, res) => {
//     res.sendFile("/public/login.html", { root: __dirname });
// });

// app.get("/viewUsers/", (req, res) => {
//     res.sendFile("/public/viewUsers.html", { root: __dirname });
// });

app.listen(port,hostname,function(){

    console.log(`Server hosted at http://${hostname}:${port}`);
});