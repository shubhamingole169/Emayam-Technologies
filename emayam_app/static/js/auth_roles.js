// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Registration Form Submission
document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
        email: formData.get('email'),
        role: formData.get('role')
    };

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (response.status === 201) {
            alert("Registration successful!");
            window.location.href = "/login-page/"; // Redirect to login page
        } else {
            const errorData = await response.json();
            alert("Registration failed: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});

// Login Form Submission
document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (response.status === 200) {
            const responseData = await response.json();
            localStorage.setItem('access_token', responseData.access);
            localStorage.setItem('refresh_token', responseData.refresh);
            alert("Login successful!");
            window.location.href = "/dashboard/"; // Redirect to dashboard
        } else {
            const errorData = await response.json();
            alert("Login failed: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});

// Check User Role and Adjust Content
async function checkUserRole() {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        alert("You are not logged in!");
        return;
    }

    try {
        const response = await fetch('/api/user/', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        });

        if (response.status === 200) {
            const userData = await response.json();
            const userRole = userData.role;

            if (userRole === 'admin' || userRole === 'editor') {
                document.getElementById('editContentButton').style.display = 'block';
            } else if (userRole === 'viewer') {
                document.getElementById('viewContentButton').style.display = 'block';
            } else {
                alert("You do not have permission to view or edit content.");
            }
        } else {
            const errorData = await response.json();
            alert("Failed to fetch user role: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
}

// On Page Load, Check User Role
document.addEventListener("DOMContentLoaded", function() {
    checkUserRole();
});
