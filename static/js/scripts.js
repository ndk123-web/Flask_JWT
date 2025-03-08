let token = "";
let refresh_attempts = 0;  // ✅ Token refresh retry limit

async function login() {

    // get the username and password from the input fields 
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;  

    // send the username and password to the server  
    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",                 // sending a post request to the server 
        headers: { "Content-Type": "application/json" }, // telling server to return a json response 
        body: JSON.stringify({ username, password }), // sending json request body 
    });

    const data = await response.json(); // getting the json response from the server 
    if (response.ok && data.access_token) {
        token = data.access_token;
        sessionStorage.setItem("access_token", data.access_token);  // ✅ sessionStorage for security
        sessionStorage.setItem("refresh_token", data.refresh_token);
        alert("Login Successfully");
    } else {
        alert(data.message || "Login Failed");
    }
}

async function get_dashboard() {
    const access_token = sessionStorage.getItem("access_token");  // getting the token from session storage 

    const response = await fetch("http://127.0.0.1:5000/dashboard", { 
        method: "GET",
        headers: { Authorization: `Bearer ${access_token}` }, // sending the token in the header to the server 
    });

    if (response.status === 401 && refresh_attempts < 2) {  
        refresh_attempts++;  // ✅ Retry token refresh once if expired
        await refresh_token();
        return get_dashboard();
    } else if (refresh_attempts >= 2) {
        alert("Session expired, login again.");
        sessionStorage.clear();
        window.location.href = "/"; // redirecting to the login page 
        return;
    }

    if (!response.ok) {  // ✅ Handle other errors
        alert("Error: " + (await response.text()));
        return;
    }

    refresh_attempts = 0;  // ✅ Reset retry count if successful
    const data = await response.json();
    alert(`${data.message} and token is ${data.token}`);
}

// refresh the token
async function refresh_token() {
    const refresh_token = sessionStorage.getItem("refresh_token");

    // if the refresh token is not present then it will alert the user to login again
    if (!refresh_token) {
        alert("Login required");
        sessionStorage.clear();
        window.location.href = "/";
        return;  // ✅ Exit function if no refresh token
    }

    // if the refresh token is present then it will refresh the token
    const response = await fetch("http://127.0.0.1:5000/refresh", {
        method: "POST",
        headers: { 
            "Authorization": `Bearer ${refresh_token}`,
            "Content-Type": "application/json"
        },
    });

    if (response.status === 401) {  // ✅ If refresh fails, clear session & logout
        sessionStorage.clear();
        window.location.href = "/";
        return;  
    }

    const data = await response.json();

    // if the token is refreshed successfully then it will store the new access token in the session storage
    if (response.ok && data.access_token) {
        sessionStorage.setItem("access_token", data.access_token);
        alert("Token refreshed!");
        return data.access_token;
    } 
    // if the token is not refreshed successfully then it will alert the user
    else {
        alert("Token refresh failed");
        sessionStorage.clear();
        window.location.href = "/";
    }
}
