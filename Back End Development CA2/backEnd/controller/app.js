//Name: Toh Kien Yu
//Class: DAAA/FT/1B/05
//Adm: 2222291

var express = require('express');
var actorDB = require('../model/actor');

var app = express();
var verifyToken = require('../auth/verifyToken')
var cors = require('cors');
app.options('*', cors());
app.use(cors())
var bodyParser = require("body-parser");
var urlencodedParser = bodyParser.urlencoded({ extended: false });
app.use(bodyParser.json());// parse application/json
app.use(urlencodedParser); // parse application/x-www-form-urlencoded

app.post('/staff/login',function (req, res) {
    var email = req.body.email;
    var password = req.body.password;
    actorDB.loginStaff(email, password, function (err, token, result) {
        if (!err) {
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            delete result[0]['password'];//clear the password in json data, do not send back to client
            console.log(result);
            res.json({ success: true, UserData: JSON.stringify(result), token: token, status: 'You are successfully logged in!' });
            res.send();
        } else {
            res.status(500);
            res.send(err.statusCode);
        }
    });
});

app.post('/staff/logout',function(req,res){
	console.log("..logging out.");
	//res.clearCookie('session-id'); //clears the cookie in the response
	//res.setHeader('Content-Type', 'application/json');
  	res.json({success: true, status: 'Log out successful!'});

});

app.post('/customer/login',function (req, res) {
    var email = req.body.email;
    var password = req.body.password;
    actorDB.loginCustomer(email, password, function (err, token, result) {
        if (!err) {
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            delete result[0]['password'];//clear the password in json data, do not send back to client
            console.log(result);
            res.json({ success: true, UserData: JSON.stringify(result), token: token, status: 'You are successfully logged in!' });
            res.send();
        } else {
            res.status(500);
            res.send(err.statusCode);
        }
    });
});

app.get("/listings", (req, res) => {
    actorDB.getListings((error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json(data);
        }
    });
});

// app.get("/search/:title", (req, res) => {
//     var title = req.params.title
//     actorDB.searchListing(title,(error, data) => {
//         if (error) {
//             console.log(error);
//             res.status(500).json({ error_msg: "Internal Server Error" });
//             return;
//         }
//         else {
//             res.status(200).json(data);
//         }
//     });
// });

app.get("/search", (req, res) => {
    var filmID = parseInt(req.query.film_id)
    actorDB.findByFilmId(filmID,(error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json(data);
        }
    });
});


app.get(`/searchs`, (req, res) => {
    var title = req.query.title
    var catid = req.query.catid
    var maxRentalRate = req.query.rentalRate


    console.log(title)
    console.log(catid)
    console.log(maxRentalRate)

    actorDB.searchFilteredListing(title,catid,maxRentalRate, (error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json({data});
        }
    });
});

app.get(`/catname`, (req, res) => {

    actorDB.getCategoryName((error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json({data});
        }
    });
});

app.get(`/filmname`, (req, res) => {
    actorDB.getFilmName((error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json({data});
        }
    });
});


app.get(`/storename`, (req, res) => {
    actorDB.getStoreName((error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json({data});
        }
    });
});

app.get(`/staffid`, (req, res) => {
    actorDB.getStaffName((error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(200).json({data});
        }
    });
});

app.post("/review", (req, res, next) => {
    if (req.body.text_body == "") {
        res.status(400).json({ error_msg: "missing data" })
        return;
    }
    actorDB.insertReview(req.body, (error, postID) => {
        console.log(req.body)
        console.log("hi")
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(201).send({postID});
    });
});


app.get("/showReview/:filmid", (req, res, next) => {
    var filmID = req.params.filmid
    actorDB.displayReview(filmID, (error, postID) => {
        console.log(filmID)
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(201).send({postID});
    });
});


app.post("/cart", (req, res, next) => {
   actorDB.insertCart(req.body, (error, postID) => {
    console.log("work")
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(201).send({postID});
    });
});

app.get("/cartDetails/:customerID", (req, res, next) => {
    var customerID = req.params.customerID
    console.log("hi")
    actorDB.getCartDetails(customerID, (error, postID) => {
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(201).send({postID});
    });
});

app.get("/getActorName", (req, res, next) => {
    actorDB.getAllActors((error, postID) => {
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(201).send({postID});
    });
});

app.delete("/customer/:customerID/film/:filmID", (req, res) => {
    const customerID = parseInt(req.params.customerID);

    const filmID = parseInt(req.params.filmID);

    actorDB.removeItem(customerID, filmID, (error) => {
        if (error) {
            console.log(error);
            res.status(500).send();
            return;
        }
        res.status(204).send();
    });
});




//Endpoint 3: Add a new actor to the database
app.post("/actors",verifyToken,(req, res) => {
    var actor = {
        first_name: req.body.first_name,
        last_name: req.body.last_name,
    }
    if (actor.first_name == "" || actor.last_name == "") {
        res.status(400).json({ error_msg: "missing data" })
        return;
    }
    actorDB.insertActor(actor, (error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            // res.setHeader('Content-Type', 'application/json');
            res.status(201).json({ actor_id: data.insertId });
        }

    });
});



//Endpoint 5: Remove Actor from database
app.delete("/actors/:actor_id/", (req, res) => {
    const actorID = parseInt(req.params.actor_id);
    actorDB.deleteActor(actorID, (error, data) => {
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else if (error == null && data == 0) {
            res.status(204).json("No Content. Record of actor_id cannot be found")
            return;
        }
        else {
            res.status(200).json({ success_msg: "actor deleted" });
        }
    });
});


//Endpoint 6: Return the film_id, title, rating, release_year and length of  all films belonging to a category.
app.get("/film_categories/:category_id", (req, res) => {
    var categoryid = req.params.category_id
    actorDB.findByCategory(categoryid, (error, data) => {
        if (isNaN(categoryid)) {
            res.status(400).json("Please enter a proper film category ID");
            return;
        }

        else if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }

        else if (error == null && data == null) {
            res.status(200).json([]);
            return;
        }

        else {
            res.status(200).json(data);
        }
    });
});

//Endpoint 7: Return the payment detail of a customer between the provided period.
app.get("/customer/:customer_id/payment", (req, res) => {
    const customerID = parseInt(req.params.customer_id);
    const datestart = req.query.start_date
    const dateend = req.query.end_date
    if (isNaN(customerID)) {
        res.status(400).send();
        return;
    }

    actorDB.findPayment(customerID, datestart, dateend, (error, data) => {
        results = JSON.parse(JSON.stringify(data))
        if (error) {
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        };
        var sum = 0
        for (var i = 0; i < results.length; i++) {
            sum += results[i].amount
        }
        res.status(200).json({ "rental": data, "total": sum.toFixed(2) });
    });
});

//Endpoint 8: Add a new customer to the database (note: customer’s email address is unique)
app.post("/customers",verifyToken, (req, res) => {
    if (req.body.store_id == "" || req.body.first_name == "" || req.body.last_name == "" || req.body.email == "" || req.body.address_line1 == "" || req.body.district == "" || req.body.city_id == "" || req.body.phone == "") {
        res.status(400).json({ error_msg: "missing_data" })
        return;
    }
    console.log(req.body)

    actorDB.addCustomer(req.body, (error, data) => {

        if (error) {
            if (error.code === "ER_DUP_ENTRY") { //If duplicate email address
                res.status(409).json({ error_msg: "email already exists" });
                return;
            }

            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(201).json(data);
            return;
        }
    });
});


//Additional Endpoint 2: Insert payment details through customerID
app.post("/payment/:customerID/", (req, res) => {
    const customerID = parseInt(req.params.customerID);
    var paymentInfo = {
        film_id: req.body.film_id,
        store_id: req.body.store_id,
        staff_id: req.body.staff_id
    }
    if (paymentInfo.film_id == "" || paymentInfo.store_id == "" || paymentInfo.staff_id == "") {
        res.status(400).json({ error_msg: "missing data" })
        return;
    }

    if (paymentInfo.film_id < 0 || paymentInfo.film_id > 1000 || paymentInfo.store_id != 1 && paymentInfo.store_id != 2 || paymentInfo.staff_id != 1 && paymentInfo.staff_id != 2) {
        res.status(400).json({ error_msg: "please input correct data" })
        return;
    }
    actorDB.insertPayment(customerID, req.body, (error, data) => {
        if (error) {
            if (error.code === "ER_NO_REFERENCED_ROW_2") {
                res.status(409).json({ error_msg: "Please enter a registered Customer ID" });
                return;
            }
            console.log(error);
            res.status(500).json({ error_msg: "Internal Server Error" });
            return;
        }
        else {
            res.status(201).json({ "Payment Detail": data });
        }

    });
});

module.exports = app;