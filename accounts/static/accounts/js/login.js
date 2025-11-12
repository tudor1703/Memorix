document.querySelector('.toggle-password').addEventListener('click', function () {
  const passwordField = document.getElementById('password');
  passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
});
