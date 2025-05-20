//Name: Toh Kien Yu
//Class: DAAA/FT/1B/05
//Adm: 2222291

const db = require("./databaseConfig");
var config = require('../config');
var jwt = require('jsonwebtoken');

const Actor = {

    loginStaff: function (email, password, callback) {

		var conn = db.getConnection();

		conn.connect(function (err) {
			if (err) {
				console.log(err);
				return callback(err, null);
			}
			else {
				console.log("Connected!");

				var sql = 'select * from staff where email=? and password=?';

				conn.query(sql, [email, password], function (err, result) {
					conn.end();

					if (err) {
						console.log("Err: " + err);
						return callback(err, null, null);
					} else {
						var token = "";
						var i;
						if (result.length == 1) {

							token = jwt.sign({ id: result[0].staff_id, role: result[0].role }, config.key, {
								expiresIn: 86400 //expires in 24 hrs
							});
							console.log("@@token " + token);
							return callback(null, token, result);


						} else {
							var err2 = new Error("UserID/Password does not match.");
							err2.statusCode = 500;
							return callback(err2, null, null);
						}
					}  //else
				});
			}
		});
	},
    
    loginCustomer: function (email, password, callback) {

		var conn = db.getConnection();

		conn.connect(function (err) {
			if (err) {
				console.log(err);
				return callback(err, null);
			}
			else {
				console.log("Connected!");

				var sql = 'select * from customer where email=? and password=?';

				conn.query(sql, [email, password], function (err, result) {
					conn.end();

					if (err) {
						console.log("Err: " + err);
						return callback(err, null, null);
					} else {
						var token = "";
						var i;
						if (result.length == 1) {

							token = jwt.sign({ id: result[0].customer_id, role: result[0].role }, config.key, {
								expiresIn: 86400 //expires in 24 hrs
							});
							console.log("@@token " + token);
							return callback(null, token, result);


						} else {
							var err2 = new Error("UserID/Password does not match.");
							err2.statusCode = 500;
							return callback(err2, null, null);
						}
					}  //else
				});
			}
		});
	},

    getListings: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const getListingsQuery = "SELECT * FROM film;";
                dbConn.query(getListingsQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    // console.log(results);
                    return callback(null, results);
                });
            }
        });
    },

    searchListing: (searchedString,callback) => {
        console.log(searchedString)
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
    
            if (err) {
                
                console.log(err);
                return callback(err, null);
            } else {
                const findByTitleQuery = `SELECT * FROM film WHERE title LIKE '%${searchedString}%';`
                dbConn.query(findByTitleQuery,[searchedString] ,(error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);
    
                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };
    
                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },
    
    
    findByFilmId: (filmID, callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findByFilmIdQuery = "SELECT film.description,film.rental_rate,actor.first_name, actor.last_name, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category, film_actor,actor WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film.film_id = film_actor.film_id AND film_actor.actor_id = actor.actor_id AND film.film_id = ?;";
                dbConn.query(findByFilmIdQuery, [filmID], (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },

    searchFilteredListing: (searchedString,catID,rentalRate,callback) => {
        console.log(searchedString)
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
    
            if (err) {
                console.log(err);
                return callback(err, null);
            } else {
                const findByTitleQuery = `SELECT * FROM film WHERE title LIKE '%${searchedString}%';`
                const findByCategoryIDQuery = "SELECT film.description,film.rental_rate, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film_category.category_id = ?;"
                const findByCategoryIDandTitleQuery = `SELECT film.description,film.rental_rate, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film_category.category_id = ? AND film.title LIKE '%${searchedString}%'`
                const findMaxRentalRateQuery = 'SELECT * from film WHERE rental_rate < ?'
                const findByCategoryIdTitleRateQuery = `SELECT film.rental_rate, film.description, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film_category.category_id = ? AND film.rental_rate <= ? AND film.title LIKE '%${searchedString}%'`
                const findByCategoryIDRentalQuery = "SELECT film.description,film.rental_rate, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film_category.category_id = ? AND film.rental_rate <= ?;"
                const findByTitleRentalQuery = `SELECT * FROM film WHERE rental_rate <= ? AND title LIKE '%${searchedString}%';`
                // const findByCategoryQuery = 'SELECT film.description, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id;'
                console.log(catID)

                // if(searchedString=='' && catID!='' &&rentalRate=='') {
                //     dbConn.query(findByCategoryQuery,(error, results) => {
                //         dbConn.end();
                //         if (error) {
                //             return callback(error, null);
        
                //         };    
                //             console.log(results.length);
                //             return callback(null, results);
                //     });
                // }

                if(searchedString != "" && catID != "" && rentalRate != "" ) {
                    dbConn.query(findByCategoryIdTitleRateQuery,[catID,rentalRate,searchedString] ,(error, results) => {
                        dbConn.end();
                        if (error) {
                            return callback(error, null);
        
                        };    
                            console.log(results.length);
                            return callback(null, results);
                    });
                }

                else if(catID == "" && searchedString != "" && rentalRate == ""){
                    dbConn.query(findByTitleQuery,[searchedString],(error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);
    
                    };    
                    // console.log(results);
                    return callback(null, results);
                });}
                else if(searchedString == "" && catID != "" && rentalRate == ""){
                    dbConn.query(findByCategoryIDQuery,[catID] ,(error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);
    
                    };    
                    console.log(results);
                    return callback(null, results);
                });}

                else if(searchedString != "" && catID != "" && rentalRate == ""){
                    dbConn.query(findByCategoryIDandTitleQuery,[catID,searchedString] ,(error, results) => {
                    if (error) {
                        return callback(error, null);
    
                    };    
                        // console.log(results);
                        return callback(null, results);
                });}

                else if(searchedString == "" && catID == "" && rentalRate != "" ) {
                    dbConn.query(findMaxRentalRateQuery,[rentalRate] ,(error, results) => {
                        if (error) {
                            return callback(error, null);
        
                        };    
                            console.log(results.length);
                            return callback(null, results);
                    });
                }

                else if(searchedString == "" && catID == "" && rentalRate != "" ) {
                    dbConn.query(findMaxRentalRateQuery,[rentalRate] ,(error, results) => {
                        if (error) {
                            return callback(error, null);
        
                        };    
                            console.log(results.length);
                            return callback(null, results);
                    });
                }

                else if(searchedString == "" && catID != "" && rentalRate != "" ) {
                    dbConn.query(findByCategoryIDRentalQuery,[catID,rentalRate] ,(error, results) => {
                        if (error) {
                            return callback(error, null);
        
                        };    
                            console.log(results.length);
                            return callback(null, results);
                    });
                }
                else if(searchedString != "" && catID == "" && rentalRate != "" ) {
                    dbConn.query(findByTitleRentalQuery,[rentalRate,searchedString] ,(error, results) => {
                        if (error) {
                            return callback(error, null);
        
                        };    
                            console.log(results.length);
                            return callback(null, results);
                    });
                }
            }
        });
    },


    getCategoryName: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findCatNameQuery = "SELECT category_id,name from category";
                dbConn.query(findCatNameQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },

    getFilmName: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findFilmNameQuery = "SELECT film_id, title from film";
                dbConn.query(findFilmNameQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },

    getStoreName: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findStoreNameQuery = "SELECT staff.store_id, address.address from address,staff WHERE address.address_id = staff.address_id";
                dbConn.query(findStoreNameQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },

    getStaffName: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findstaffIdQuery = "SELECT staff.staff_id,staff.first_name, staff.last_name from staff";
                dbConn.query(findstaffIdQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },


    insertReview: function (review, callback) {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {//database connection gt issue!

                console.log(err);
                return callback(err, null);
            } else {
                const insertReviewQuery =`INSERT INTO review (customer_id,film_id,text_body) VALUES (?,?,?);`;
                
                dbConn.query(insertReviewQuery, [review.customer_id,review.film_id, review.text_body], (error, results) => {
                    dbConn.end()
                    if (error) {
                        return callback(error, null);
                    }
                    return callback(null, results);
                });
            }
        });
    },

    
    displayReview: function (filmID, callback) {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {//database connection gt issue!

                console.log(err);
                return callback(err, null);
            } else {
                // const displayReviewQuery =`SELECT text_body, c.first_name,c.last_name FROM review r, customer c WHERE c.customer_id = r.customer_id AND r.film_id = ?`;
                const displayReviewQuery =`SELECT text_body, c.first_name,c.last_name FROM review r, customer c WHERE c.customer_id = r.customer_id AND r.film_id = ?`;              
                dbConn.query(displayReviewQuery, [filmID], (error, results) => {
                    dbConn.end()
                    if (error) {
                        return callback(error, null);
                    }
                    return callback(null, results);
                });
            }
        });
    },


    insertCart: function (cart, callback) {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {//database connection gt issue!

                console.log(err);
                return callback(err, null);
            } else {
                const insertReviewQuery =`INSERT INTO cart (customer_id,film_id,amount) VALUES (?,?,?);`;
                
                dbConn.query(insertReviewQuery, [cart.customer_id,cart.film_id, cart.amount], (error, results) => {
                    dbConn.end()
                    if (error) {
                        return callback(error, null);
                    }
                    return callback(null, results);
                });
            }
        });
    },

    getCartDetails: (customerID,callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const getCartDetailsQuery = "SELECT * FROM film,cart WHERE film.film_id = cart.film_id AND cart.customer_id = ? ";
                dbConn.query(getCartDetailsQuery,[customerID] ,(error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },


    removeItem: function (customerID, filmID, callback) {

        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {//database connection gt issue!

                console.log(err);
                return callback(err, null);
            } else {
                const deleteFromCartQuery =`DELETE FROM cart WHERE customer_id = ? AND film_id = ?;`;
                dbConn.query(deleteFromCartQuery, [customerID, filmID], (error, results) => {
                    if (error) {
                        return callback(error);
                    }
                    return callback(null);
                });
            }
        });
    },

    //Endpoint 3: Add a new actor to the database
    insertActor: (actor, callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {                
                const updateActorQuery = "INSERT INTO actor (first_name, last_name) VALUES (?,?)";
                dbConn.query(updateActorQuery, [actor.first_name, actor.last_name], (error, results) => {
                    dbConn.end();
                    if (error) {
                        console.log(error);
                        return callback(error, null);

                    };
                    if (actor.first_name == "" || actor.last_name == "") {
                        callback(null, null);
                        return;
                    };
                    console.log(results);
                    return callback(null, results);
                }); 
            }
        });
    },

    getAllActors: (callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findActorNameQuery = "SELECT * from actor"
                dbConn.query(findActorNameQuery, (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },





        //Endpoint 5: Remove Actor from database
        deleteActor: (actorID, callback) => {
            var dbConn = db.getConnection();
            dbConn.connect(function (err) {
                if (err) {
                    console.log(err);
                    return callback(err, null);
                } else {
                    const deleteFkActorQuery = "DELETE FROM film_actor WHERE film_actor.actor_id = ?";
                    const deletePkActorQuery = "DELETE FROM actor WHERE actor.actor_id = ?";
                    dbConn.query(deleteFkActorQuery, [actorID], (error, results) => {
                        if (error) {
                            return callback(error, null);
                        };
                        console.log(results)
                        dbConn.query(deletePkActorQuery, [actorID], (error, results) => {
                            dbConn.end();
                            if (error) {
                                return callback(error, null);
                            };
        
                            console.log(results)
                            return callback(null, results.affectedRows);
                        })
                    });
                }
            });
        },

    
    //Endpoint 6: Return the film_id, title, rating, release_year and length of  all films belonging to a category.
    findByCategory: (categoryID, callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {

            if (err) {

                console.log(err);
                return callback(err, null);
            } else {
                const findByCategoryIDQuery = "SELECT film.description, film.film_id, film.title, category.name as category, film.rating, film.release_year, film.length as duration FROM film, film_category, category WHERE film_category.film_id = film.film_id AND film_category.category_id = category.category_id AND film_category.category_id = ?;"
                dbConn.query(findByCategoryIDQuery, [categoryID], (error, results) => {
                    dbConn.end();
                    if (error) {
                        return callback(error, null);

                    };
                    if (results.length === 0) {
                        callback(null, null);
                        return;
                    };

                    console.log(results);
                    return callback(null, results);
                });
            }
        });
    },


    //Endpoint 8: Add a new customer to the database (note: customer’s email address is unique)
    addCustomer: (customerInfo,callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err, null);
            } else {        
                const addCustomerQuery = "INSERT INTO customer (store_id, first_name, last_name, email, address_id,password) VALUES (?,?,?,?,?,?);";
                const addAddressQuery = "INSERT INTO address (address, address2, district,city_id, postal_code, phone) VALUES (?,?,?,?,?,?);"
                const showResultsQuery = "SELECT c.customer_id FROM customer c, address a WHERE c.address_id = a.address_id and a.address_id = ?"    
                dbConn.query(addAddressQuery, [customerInfo.address_line1,customerInfo.address_line2,customerInfo.district,customerInfo.city_id,customerInfo.postal_code,customerInfo.phone], (error, results) => {

                    if (error) {
                        return callback(error, null);
                    };
                    insertedID = results.insertId
                    dbConn.query(addCustomerQuery, [customerInfo.store_id,customerInfo.first_name.toUpperCase(), customerInfo.last_name.toUpperCase(),customerInfo.email,insertedID,customerInfo.password], (error, results) => {

                        if (error) {

                            return callback(error, null);
                    
                        };
                        
                        dbConn.query(showResultsQuery, [insertedID], (error, results) => {

                            dbConn.end();
                            if (error) {
                                return callback(error, null);
                        
                            };

                            return callback(null, results);
                        }); 
                    });    
                    
                }); 
            }
        });
    },

    //Additional Endpoint 2: Insert payment details through customerID
    insertPayment: (customerID, paymentInfo, callback) => {
        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
            if (err) {
                return callback(err, null);
            } else {       
                const getInventoryIdQuery = "INSERT INTO inventory (film_id, store_id) VALUES (?,?)";
                const getRentalIdQuery = "INSERT INTO rental (inventory_id, customer_id, staff_id) VALUES (?,?,?)";
                const getAmountQuery = "SELECT film.rental_rate FROM film where film_id = ?"
                const insertPaymentInfoQuery = "INSERT into payment(customer_id, staff_id, rental_id, amount) VALUES (?,?,?,?)"
                const getPaymentDetails = "SELECT payment.customer_id, customer.first_name, customer.last_name, rental_id, amount, payment_date FROM payment, customer WHERE payment.customer_id = customer.customer_id and payment_id = ? "
                dbConn.query(getInventoryIdQuery, [paymentInfo.film_id, paymentInfo.store_id], (error, results) => {
                    if (error) {
                        return callback(error, null);
                    };
                    inventoryID = results.insertId
                    dbConn.query(getRentalIdQuery, [inventoryID, customerID, paymentInfo.staff_id], (error, results) => {
                        if (error) {
                            return callback(error, null);
    
                        };

                        rentalID = results.insertId
                        
                        dbConn.query(getAmountQuery, [paymentInfo.film_id], (error, results) => {
                            if (error) {
                                return callback(error, null);
                            };
                            amountIncurred = results[0]['rental_rate']
                            dbConn.query(insertPaymentInfoQuery, [customerID,paymentInfo.staff_id,rentalID, amountIncurred], (error, results) => {

                                if (error) {
                                    return callback(error, null);
                                };
                                insertedRow = results.insertId

                                dbConn.query(getPaymentDetails, [insertedRow], (error, results) => {
                                    dbConn.end();
                                    if (error) {
                                        return callback(error, null);
                                    };
                                    return callback(null, results);
                                });
                            });
                        });
                    }); 
                }); 
            }
        });
    },
};

module.exports = Actor;
