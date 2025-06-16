document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('loginForm');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const username = document.getElementById('username').value.trim();
      const password = document.getElementById('password').value;

      // Check localStorage accounts
      let accounts = JSON.parse(localStorage.getItem('accounts') || '[]');
      const found = accounts.find(acc => acc.username === username && acc.password === password);

      // Default super admin account
      if (username === "admin" && password === "admin") {
        localStorage.setItem('currentUser', username);
        localStorage.setItem('currentRole', 'superadmin');
        window.location.href = "Dashboard.html";
      } else if (found) {
        localStorage.setItem('currentUser', username);
        localStorage.setItem('currentRole', found.role || 'user'); // Use role from account
        window.location.href = "Dashboard.html";
      } else {
        alert("Invalid username or password.");
      }
    });
  }
});