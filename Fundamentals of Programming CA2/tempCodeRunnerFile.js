// Name  : Toh Kien Yu
// Class : DCITP/FT/1A/02
// Adm   : 2222291

var input = require("readline-sync");

class Member {
    constructor(name, membershipType, dateJoined, dateOfBirth, points, voucher, status) {
        this.name = name;
        this.membershipType = membershipType;
        this.dateJoined = dateJoined;
        this.dateOfBirth = dateOfBirth;
        this.points = points;
        this.voucher = voucher;
        this.status = status;
    }

    //Prints a member information
    getMemberInfo() {
        var s = "";
        s += "\nName: " + this.name;
        s += "\nMembership Type: " + this.membershipType;
        s += "\nDate Joined: " + this.dateJoined;
        s += "\nDate Of Birth: " + this.dateOfBirth;
        s += "\nPoints Earned: " + this.points;
        s += "\nVouchers Earned: " + this.voucher;
        s += "\nMembership Status: " + this.status;
        return s;
    }
}

class MemberGroup {
    constructor() {
        this.memberList = [];
        this.memberList.push(new Member("Leonardo", "Gold", "1 Dec 2019", "1 Jan 1980", 1400, 0, "Active"));
        this.memberList.push(new Member("Catherine", "Ruby", "14 Jan 2020", "28 Oct 1985", 250, 0, "Active"));
        this.memberList.push(new Member("Luther", "Gold", "29 Apr 2020", "16 Mar 1992", 3350, 0, "Active"));
        this.memberList.push(new Member("Bruce", "Diamond", "3 Jun 2020", "18 Mar 1994", 40200, 0, "Active"));
        this.memberList.push(new Member("Amy", "Ruby", "5 Jun 2020", "31 May 2000", 500, 0, "Active"));
    }

    //Return number of members in list
    getNumberOfMembers() {
        return this.memberList.length;
    }

    //Prints Every member's information
    getAllMemberInfo() {
        //For loop and get details of each and every member
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            console.log("\nName: " + this.memberList[i].name);
            console.log("Membership Type: " + this.memberList[i].membershipType);
            console.log("Date joined: " + this.memberList[i].dateJoined);
            console.log("Date of Birth: " + this.memberList[i].dateOfBirth);
            console.log("Points Earned: " + this.memberList[i].points);
            console.log("Vouchers Earned: " + this.memberList[i].voucher);
            console.log("Membership status: " + this.memberList[i].status);
        }
    }

    //Search for member and verify if member exists
    displayMember(name) {
        //For loop to ensure that member name exists in the database before providing the specific member's information
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If member's name equals to the name input
            if (this.memberList[i].name.toLowerCase() == name) {
                return this.memberList[i].getMemberInfo();
            }
        }
        return "Member does not exist.";
    }

    //Searches for member with same name before adding member
    searchMember(name) {
        //For loop to check and ensure that name entered will not match any of the existing member's name
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If member's name equals to the name input
            if (this.memberList[i].name.toLowerCase() == name) {
                return "\nMember\'s name exists in database. Please enter a new name.\n";
            }
        }
        return "Member List Updated!\n";
    }

    //Searches for member with same name before updating points earned in the user's account
    updatePoints(name) {
        var added = 0;
        //For loop to check if name entered matches the existing member's name before being allowed to add points into user's account
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If member's name equates to the name input
            if (this.memberList[i].name.toLowerCase() == name) {
                var amountSpent = input.question("Please enter your amount spent: ");
                var pointsEarned = this.memberList[i].points;
                if (parseFloat(amountSpent) == amountSpent) {
                    switch (true) {
                        case (amountSpent >= 2500.01):
                            added = 2000;
                            pointsEarned += 2000;
                            break;

                        case (1000.01 <= amountSpent && amountSpent <= 2500):
                            added = 1000;
                            pointsEarned += 1000;
                            break;

                        case (500.01 <= amountSpent && amountSpent <= 1000):
                            added = 500;
                            pointsEarned += 500;
                            break;

                        case (200.01 <= amountSpent && amountSpent <= 500):
                            added = 200;
                            pointsEarned += 200;
                            break;

                        case (100.01 <= amountSpent && amountSpent <= 200):
                            added = 100;
                            pointsEarned += 100;
                            break;

                        case (50.01 <= amountSpent && amountSpent <= 100):
                            added = 50;
                            pointsEarned += 50;
                            break;

                        case (amountSpent <= 50):
                            added = 10;
                            pointsEarned += 10;
                            break;
                    }
                    this.memberList[i].points = pointsEarned;
                    return "\n" + added + " Points have been added.\nTotal Points Earned: " + this.memberList[i].points;
                }
                else {
                    return "Please enter a valid amount.";
                }
            }
        }
        return "Member does not exist.";
    }

    //Update Membership Type
    updateRank() {
        //For loop to update the membership type of all the existing members
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            switch (true) {
                case (this.memberList[i].points >= 20000):
                    this.memberList[i].membershipType = "Diamond";
                    break;

                case (5000 <= this.memberList[i].points && this.memberList[i].points <= 19999):
                    this.memberList[i].membershipType = "Platinum";
                    break;

                case (500 <= this.memberList[i].points && this.memberList[i].points <= 4999):
                    this.memberList[i].membershipType = "Gold";
                    break;

                default: this.memberList[i].membershipType = "Ruby";
                    break;
            }

        }
    }

    //Find and display the youngest and oldest member
    memberAges() {
        var oldest = "";
        var youngest = "";
        var comparing = 0;
        var a = 99999999999;
        var b = 0;

        //For loop to find out every member's date of birth one by one before determining which member is the youngest and oldest
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            var currentDate = new Date();
            var memberAge = (currentDate - new Date(this.memberList[i].dateOfBirth)) - 1;
            var memberAgeInDays = memberAge / 1000 / 60 / 60 / 24;

            comparing = memberAgeInDays;
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If member's age is younger than the previous member
                if (comparing < a) {
                    a = comparing;
                    youngest = this.memberList[i].name;
                }
                //If the youngest's member age is the same as the previous member
                else if (comparing == a) {
                    youngest += ", " + this.memberList[i].name;
                }
                //If member's age is older than the previous member
                if (comparing > b) {
                    b = comparing;
                    oldest = this.memberList[i].name;
                }
                //If the oldest's member age is the same as the previous member
                else if (comparing == b) {
                    oldest += ", " + this.memberList[i].name;
                }
            }
        }
        return "\nYoungest member : " + youngest.charAt(0).toUpperCase() + youngest.slice(1).toLowerCase() + "\nOldest member   : " + oldest.charAt(0).toUpperCase() + oldest.slice(1).toLowerCase();
    }

    //Find and display the member with the highest and lowest point
    highestLowestPoints() {
        var highest = 0;
        var smallest = 10000000;
        var highestPoint = "";
        var lowestPoint = "";
        //For loop to find out every member's point one by one before determining which member has the highest or lowest point
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            var memberPoints = this.memberList[i].points;
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If member's point is lower than the previous member
                if (memberPoints < smallest) {
                    smallest = memberPoints;
                    lowestPoint = this.memberList[i].name;
                }
                //If member's point is the same as the previous smallest point
                else if (memberPoints == smallest) {
                    lowestPoint += ", " + this.memberList[i].name;
                }
                
                //If member's point is higher than the previous member
                if (memberPoints > highest) {
                    highest = memberPoints;
                    highestPoint = this.memberList[i].name;
                }
                //If member's point is the same as the previous highest point
                else if (memberPoints == highest) {
                    highestPoint += ", " + this.memberList[i].name;
                }
            }
        }
        return "\nHighest member  : " + highestPoint.charAt(0).toUpperCase() + highestPoint.slice(1).toLowerCase() + "\nLowest member   : " + lowestPoint.charAt(0).toUpperCase() + lowestPoint.slice(1).toLowerCase();
    }

    //Display total number of members in same rank
    membersInSameRank() {
        var ruby = 0;
        var gold = 0;
        var platinum = 0;
        var diamond = 0;
        //For loop to find out about every member's membership type, each membership type will increment once whenever a member is in that rank. The total number of members in each membership type will then be determined
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If membership type is Ruby
                if (this.memberList[i].membershipType == "Ruby") {
                    ++ruby;
                }
                //If membership type is Gold
                else if (this.memberList[i].membershipType == "Gold") {
                    ++gold;
                }
                //If membership type is Platinum
                else if (this.memberList[i].membershipType == "Platinum") {
                    ++platinum;
                }
                //If membership type is Diamond
                else if (this.memberList[i].membershipType == "Diamond") {
                    ++diamond;
                }
            }
        }
        return "\nTotal number of members in each Membership Type:\nRuby: " + ruby + "\nGold: " + gold + "\nPlatinum: " + platinum + "\nDiamond: " + diamond;
    }

    //Display total points in each membership type
    totalPoints() {
        var rubyPoints = 0;
        var goldPoints = 0;
        var platinumPoints = 0;
        var diamondPoints = 0;
        //For loop to find out about every member's points and add up the total points for the different types of membership rank
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If membership type is Ruby
                if (this.memberList[i].membershipType == "Ruby") {
                    rubyPoints += this.memberList[i].points;
                }
                //If membership type is Gold
                else if (this.memberList[i].membershipType == "Gold") {
                    goldPoints += this.memberList[i].points;
                }
                //If membership type is Platinum
                else if (this.memberList[i].membershipType == "Platinum") {
                    platinumPoints += this.memberList[i].points;
                }
                //If membership type is Diamond
                else if (this.memberList[i].membershipType == "Diamond") {
                    diamondPoints += this.memberList[i].points;
                }
            }
        }
        return "\nTotal Points in each Membership Type:\nRuby     : " + rubyPoints + "\nGold     : " + goldPoints + "\nPlatinum : " + platinumPoints + "\nDiamond  : " + diamondPoints;
    }

    //Update Vouchers, (A voucher is given at the user's birth month every year)
    updateVouchers() {
        var currentMonth = new Date().getMonth();
        var monthName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var month = monthName[new Date().getMonth()];
        //For loop to check for every member's date of birth's month, then rewarding the user with a voucher during their birth's month 
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            var memberDateOfBirth = this.memberList[i].dateOfBirth;
            var memberMonth = new Date(memberDateOfBirth).getMonth();
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If member's date of birth month is the same as the current month
                if (memberMonth == currentMonth) {
                    ++this.memberList[i].voucher;
                }
            }
        }
        return "Vouchers updated to the " + month + " babies.";
    }

    removeMember() {
        var remove = input.question("Enter member\'s name to be removed: ");
        //For loop to check if the input matches existing member's name before removing that member from the system.
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If existing member's name equates to the name input
            if (this.memberList[i].name.toLowerCase() == remove.toLowerCase()) {
                this.memberList[i].status = "Expired";
                return "Member: " + remove.charAt(0).toUpperCase() + remove.slice(1).toLowerCase() + " has been removed.";
            }
        }
        return "Member does not exists.";
    }

    highestVoucher() {
        var highest = 0;
        var highestVoucher = "";
        //For loop to find out the number of vouchers every member have before determining who has the most number of vouchers
        for (var i = 0; i < this.getNumberOfMembers(); i++) {
            //If membership status is active
            if (this.memberList[i].status == "Active") {
                //If member's voucher is higher than the previous member's amount of voucher
                if (this.memberList[i].voucher > highest) {
                    highest = this.memberList[i].voucher;
                    highestVoucher = this.memberList[i].name;
                }
                //If member's voucher is the same as the previous member's amount of voucher
                else if (this.memberList[i].voucher == highest) {
                    highestVoucher += "  " + this.memberList[i].name;
                }
            }
        }
        return "\nMember with highest voucher: " + highestVoucher;
    }

}

//Prints Display Menu
function displayMenu() {
    console.log("\nHi, " + nameEntered + " please select your choices:");
    console.log("\t1. Display all members\' information");
    console.log("\t2. Display member information");
    console.log("\t3. Add new member");
    console.log("\t4. Update points earned");
    console.log("\t5. Statistics");
    console.log("\t6. Update Vouchers.");
    console.log("\t7. Remove a member");
    console.log("\t8. Exit");
}

//Prints Sub-Menu
function displaySubMenu() {
    console.log("\n\tPlease select an option from the sub-menu:");
    console.log("\t1. Display names of (all) a certain type of members only.");
    console.log("\t2. Display the name of the youngest and oldest member in the system.");
    console.log("\t3. Display the name of members with the highest and lowest points earned.");
    console.log("\t4. Display total number of members in each membership type.");
    console.log("\t5. Display the total points in each membership type.");
    console.log("\t6. Display the member with the highest voucher received");
    console.log("\t7. Return to main-menu");
}

//Prompt User Input for Name
function promptInput() {
    var inputEntered = input.question("Please enter your name: ");
    return inputEntered.toLowerCase();
}

//Search for member and display Member's Information
function search() {
    var nameEntered = promptInput();
    var s = myMemberGroup.displayMember(nameEntered);
    return s;
}

//Checks if name is already used by someone else in Database
function checkData(name) {
    var k = myMemberGroup.searchMember(name);
    return k;
}



//--------------------------------------------------------------------------------------------
//Main Programme
var myMemberGroup = new MemberGroup();
console.log("Welcome to XYZ Membership Loyalty Programme!");
var nameEntered = input.question("Please enter your name: ");

do {
    //Display Main-Menu
    displayMenu();
    var directory = input.question("\t>> ");
    myMemberGroup.updateRank();

    //If user does not input a valid input (1-8) in the Main-Menu
    if (directory != 1 && directory != 2 && directory != 3 && directory != 4 && directory != 5 && directory != 6 && directory != 7 && directory != 8) {
        console.log("Please enter a valid input.\n");
    }

    //User Inputs 1 in the Main-Menu
    else if (directory == 1) {
        myMemberGroup.getAllMemberInfo();
    }
    //User Inputs 2 in the Main-Menu
    else if (directory == 2) {
        var searched = search();
        console.log(searched);
    }

    //User Inputs 3 in the Main-Menu
    else if (directory == 3) {
        do {
            var nameToBeChecked = promptInput();
            var memberName = checkData(nameToBeChecked);
            console.log(memberName);
        } while (memberName != "Member List Updated!\n");

        var r = input.question("Please enter member\'s date of birth: ");
        console.log("Date of Birth Updated!");
        var monthName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var month = monthName[new Date().getMonth()];
        myMemberGroup.memberList.push(new Member(nameToBeChecked.charAt(0).toUpperCase() + nameToBeChecked.slice(1).toLowerCase(), "Ruby", new Date().getDate() + " " + month + " " + new Date().getFullYear(), r, 0, 0, "Active"));
    }

    //User Inputs 4 in the Main-Menu
    else if (directory == 4) {
        var check = promptInput();
        var pointsEarned = myMemberGroup.updatePoints(check);
        console.log(pointsEarned);
    }

    //User Inputs 5 in the Main-Menu
    else if (directory == 5) {
        do {
            //Displays Sub-Menu
            displaySubMenu();
            var subDirectory = input.question("\t>> ");

            //If user does not input a valid input (1-7) in the Sub-Menu
            if (subDirectory != 1 && subDirectory != 2 && subDirectory != 3 && subDirectory != 4 && subDirectory != 5 && subDirectory != 6 && subDirectory != 7) {
                console.log("\n\tPlease enter a valid input.\n");
            }

            //User Inputs 1 in Sub-Menu
            if (subDirectory == 1) {
                do {
                    var membType = input.question("Enter Membership Type: ");
                    //If user does not enter a valid membership type
                    if (membType.toLowerCase() != "ruby" && membType.toLowerCase() != "gold" && membType.toLowerCase() != "platinum" && membType.toLowerCase() != "diamond") {
                        console.log("Please enter a valid membership type.");
                        var f = 0;
                    }
                    else {
                        var isInside = false;
                        var membersInSameRank = "";
                        //For loop to find out about member's membership type and display the members found in that specific membership type
                        for (var i = 0; i < myMemberGroup.getNumberOfMembers(); i++) {
                            //If membership status is active
                            if (myMemberGroup.memberList[i].status == "Active") {
                                //If existing membership type is the same as the membership type entered
                                if (myMemberGroup.memberList[i].membershipType.toLowerCase() == membType.toLowerCase()) {
                                    isInside = true;
                                    membersInSameRank += myMemberGroup.memberList[i].name + "  ";
                                }
                            }
                            var f = 1;
                        }
                        //If isInside equals false
                        if (isInside == false) {
                            console.log("No Members found in " + membType.charAt(0).toUpperCase() + membType.slice(1).toLowerCase() + ".");
                        }
                        else {
                            console.log("Number(s) of membership type " + membType.charAt(0).toUpperCase() + membType.slice(1).toLowerCase() + ": " + membersInSameRank);
                        }
                    }

                } while (f == 0);
            }

            //User Inputs 2 in Sub-Menu
            else if (subDirectory == 2) {
                console.log(myMemberGroup.memberAges());
            }

            //User Inputs 3 in Sub-Menu
            else if (subDirectory == 3) {
                console.log(myMemberGroup.highestLowestPoints());
            }

            //User Inputs 4 in Sub-Menu
            else if (subDirectory == 4) {
                console.log(myMemberGroup.membersInSameRank());
            }

            //Usere Inputs 5 in Sub-Menu
            else if (subDirectory == 5) {
                console.log(myMemberGroup.totalPoints());
            }

            //User Inputs 6 in Sub-Menu
            else if (subDirectory == 6) {
                console.log(myMemberGroup.highestVoucher());
            }

        } while (subDirectory != 7); //User inputs 7 and exits the Sub-Menu
    }

    //User inputs 6 in the Main-Menu. Vouchers to be updated at every first day of the month. User receives a voucher during their birthday month
    else if (directory == 6) {
        console.log(myMemberGroup.updateVouchers());
    }

    //User inputs 7 in the Main-Menu
    else if (directory == 7) {
        console.log(myMemberGroup.removeMember());
    }

} while (directory != 8); // User inputs 8 and exits the Main-Menu


//Prints Good Bye Messege
console.log("\nThank you and Good Bye!");
