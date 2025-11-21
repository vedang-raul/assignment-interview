const API_URL = "http://127.0.0.1:8000/api/v1";

// --- HELPER: DECODE JWT (To read the Role) ---
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return {};
    }
}

// --- AUTHENTICATION FUNCTIONS ---

function toggleForms() {
    document.getElementById("login-form").classList.toggle("hidden");
    document.getElementById("register-form").classList.toggle("hidden");
    document.getElementById("auth-msg").innerText = "";
}

async function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-pass").value;
    const msg = document.getElementById("auth-msg");

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            
            // EXTRACT & SAVE ROLE
            const payload = parseJwt(data.access_token);
            localStorage.setItem("role", payload.role); // "admin" or "user"

            window.location.href = "dashboard.html";
        } else {
            msg.innerText = "Login failed: " + (data.detail || "Unknown error");
        }
    } catch (e) {
        msg.innerText = "Cannot connect to server.";
        console.error(e);
    }
}

async function register() {
    // 1. GET ELEMENTS (Not just values)
    const usernameInput = document.getElementById("reg-username");
    const emailInput = document.getElementById("reg-email");
    const passwordInput = document.getElementById("reg-pass");
    const adminCodeInput = document.getElementById("reg-admin");
    const msg = document.getElementById("auth-msg");

    // 2. EXTRACT VALUES FOR PAYLOAD
    const payload = { 
        username: usernameInput.value, 
        email: emailInput.value, 
        password: passwordInput.value 
    };
    
    if (adminCodeInput.value) payload.admin_code = adminCodeInput.value;

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            alert("Registration successful! Please Login.");
            
            // 3. CLEAR THE ELEMENTS (Now this variable exists!)
            usernameInput.value = "";
            emailInput.value = "";
            passwordInput.value = "";
            adminCodeInput.value = "";
            
            toggleForms(); // Switch to login view
        } else {
            msg.innerText = data.detail || "Registration failed";
        }
    } catch (e) { msg.innerText = "Cannot connect to server."; }
}


function logout() {
    localStorage.clear(); // Clears token AND role
    window.location.href = "index.html";
}

// --- RBAC UI LOGIC ---

function applyRoleBasedUI() {
    const role = localStorage.getItem("role");
    const createSection = document.getElementById("create-task-section");
    
    // If we are on the dashboard and the user is NOT an admin
    if (createSection && role !== 'admin') {
        createSection.style.display = 'none'; // Hide the Create Form
    }
}

// --- TASK MANAGEMENT FUNCTIONS ---

async function fetchTasks() {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role"); // Get role for button logic
    const container = document.getElementById("tasks-container");

    try {
        const res = await fetch(`${API_URL}/tasks/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.status === 401) { logout(); return; } // Token expired

        const tasks = await res.json();
        container.innerHTML = ""; // Clear loading text

        if (tasks.length === 0) {
            container.innerHTML = '<div style="text-align:center; color:#999;">No tasks found.</div>';
            return;
        }

        tasks.forEach(task => {
            const div = document.createElement("div");
            div.className = `task-item ${task.completed ? 'completed' : ''}`;
            
            // LOGIC: Only show Delete button if Admin
            const deleteBtn = role === 'admin' 
                ? `<button class="btn-del" onclick="deleteTask('${task._id}')">✕</button>` 
                : '';

            // LOGIC: Everyone can mark complete (unless already done)
            const doneBtn = !task.completed 
                ? `<button class="btn-done" onclick="completeTask('${task._id}')">✓</button>` 
                : '';

            div.innerHTML = `
                <div class="task-content">
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                </div>
                <div class="task-actions">
                    ${doneBtn}
                    ${deleteBtn} 
                </div>
            `;
            container.appendChild(div);
        });
    } catch (e) {
        console.error(e);
    }
}

async function createTask() {
    const title = document.getElementById("task-title").value;
    const desc = document.getElementById("task-desc").value;
    const token = localStorage.getItem("token");

    if (!title || !desc) return alert("Please fill in both fields.");

    const res = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ title: title, description: desc })
    });

    if (res.ok) {
        document.getElementById("task-title").value = "";
        document.getElementById("task-desc").value = "";
        fetchTasks(); // Refresh list
    } else {
        const data = await res.json();
        alert(data.detail); // Show "Only Admins..." error
    }
}

async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) return;

    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
        fetchTasks();
    } else {
        const data = await res.json();
        alert(data.detail); // Show "Only Admins..." error
    }
}

async function completeTask(id) {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: { 
            "Content-Type": "application/json", 
            "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ completed: true })
    });

    if (res.ok) fetchTasks();
    else alert("Failed to update task.");
}