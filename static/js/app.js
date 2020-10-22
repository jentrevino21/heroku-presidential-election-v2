// Create machine learning function
async function initiateModel(zipInput, employmentInput, amountInput) {
    const responseData = await d3.json("https://presidential-election-analysis.herokuapp.com/" + zipInput + "/" + employmentInput + "/" + amountInput).then(responseData => displayResults(responseData));
    console.log(responseData);

};


// Create function for displaying results
function displayResults(jsonResponse) {
    console.log(jsonResponse[0]);

    var politicalParty = jsonResponse[0]["Campaign"];
    console.log(politicalParty);

    if (politicalParty = "Democrat") {
        var president = "Joe Biden";
        var presidentImg = "./static/images/biden_choice.png"
    }else{
        var president = "Donald Trump";
        var presidentImg = "./static/images/trump_choice.png"
    };

    // Display results
    d3.selectAll("#results_text_one")
        .append("text")
        .text(`Looks like you support ${ president }!`);

    d3.selectAll("#results_text_two")
        .append("text")
        .text(`We are 82.3 % confident in this projection.`);

    var resultsHTML = d3.select("#results_html");
    
    resultsHTML.append("img")
        .attr("src", `${ presidentImg }`)
        .classed("img-fluid");
};

// Locate submission button
var submitButton = d3.select("#submit_button");

// Create function to process form entries
function handleChange(event) {

    // event.preventDefault();
    
    // Locate input data
    var zipInput = d3.select("#input_zip").property("value");
    var employmentInput = d3.select("#select_occupation").property("value");
    var amountInput = d3.select("#input_amount").property("value");

    // Display input data on console
    console.log(zipInput);
    console.log(employmentInput);
    console.log(amountInput);
    console.log(typeof(zipInput));
    console.log(typeof(employmentInput));
    console.log(typeof(amountInput));

    // Use input data to initiate machine learning function
    initiateModel(zipInput, employmentInput, amountInput);
};
