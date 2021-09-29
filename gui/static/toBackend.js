function send_elem_creation(ID){
    fetch('/', {

        // Declare what type of data we're sending
        headers: {
          'Content-Type': 'application/json',
          'Action-Type': 'elementCreate'
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify({id: ID})
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ' + text);

    });
}

function send_elem_change(ID){
    fetch('/', {

        // Declare what type of data we're sending
        headers: {
          'Content-Type': 'application/json',
          'Action-Type': 'elementChange'
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify(elements[ID])
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ' + text);

    });
}

function update_graph(){
    fetch('/', {

        // Declare what type of data we're sending
        headers: {
          'Content-Type': 'application/json',
          'Action-Type': 'graph'
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify(directedGraph)
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ' + text);

    });
}