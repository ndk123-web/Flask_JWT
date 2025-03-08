let token = "";

async function login() {

    // get the username and password from the input fields 
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;  

    // send the username and password to the server  
    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",                 // sending a post request to the server 
        headers: { "Content-Type": "application/json" }, // telling server to return a json response 
        // converting Object into JSON String so that Server will understand
        body: JSON.stringify({ username: username, password: password }), // sending json request body 
    });

    const data = await response.json(); // getting the json response from the server 
    if (response.ok && data.access_token) {
        token = data.access_token;
        localStorage.setItem("jwt", token);   // storing the token in the local storage 
        alert("Login Successfully");
    } else {
        alert(data.message || "Login Failed");
    }
}

async function get_dashboard() {
    const savedtoken = localStorage.getItem("jwt");  // getting the token from the local storage 

    if (!savedtoken) {
        alert("Login required");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/dashboard", { 
        method: "GET",
        headers: { Authorization: `Bearer ${savedtoken}` }, // sending the token in the header to the server 
    });

    const data = await response.json();
    alert(`${data.message} and token is ${data.token}`);
}
