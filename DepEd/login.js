document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        const result = await response.json();
        if (response.ok && result.status === 'success') {
          localStorage.setItem('currentUser', username);
          localStorage.setItem('currentRole', result.role); // 'admin' or 'user'
          window.location.href = "Dashboard.html";
        } else {
          alert("Invalid username or password.");
        }
      } catch (err) {
        alert("Server error. Please try again.");
      }
    });
  }
});