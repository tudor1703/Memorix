
document.addEventListener('DOMContentLoaded', () => {
  const googleBtn = document.getElementById('googleBtn');
  const fbBtn = document.getElementById('fbBtn');
  const togglePwd = document.getElementById('togglePwd');
  const passwordInput = document.getElementById('password');
  const form = document.getElementById('signupForm');
  const createBtn = document.getElementById('createBtn');

  googleBtn.addEventListener('click', () => {
    alert('Simulare: autentificare cu Google (doar demo).');
  });
  fbBtn.addEventListener('click', () => {
    alert('Simulare: autentificare cu Facebook (doar demo).');
  });

  togglePwd.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      togglePwd.textContent = '🙈';
    } else {
      passwordInput.type = 'password';
      togglePwd.textContent = '👁️';
    }
  });

  function loadUsers(){
    try {
      const raw = localStorage.getItem('memoriX_users');
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }
  function saveUsers(users){
    localStorage.setItem('memoriX_users', JSON.stringify(users));
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const first = document.getElementById('first').value.trim();
    const last = document.getElementById('last').value.trim();
    const email = document.getElementById('email').value.trim();
    const pwd = passwordInput.value;
    const agree = document.getElementById('agree').checked;

    if (!first || !last || !email || !pwd) {
      alert('Completează toate câmpurile obligatorii.');
      return;
    }
    if (!agree) {
      alert('Trebuie să accepți Termenii și Politica de confidențialitate.');
      return;
    }
    const emReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emReg.test(email)) {
      alert('Introdu o adresă de email validă.');
      return;
    }

    createBtn.disabled = true;
    createBtn.textContent = 'Creating...';

    setTimeout(() => {
      const users = loadUsers();

      if (users.some(u => u.email.toLowerCase() === email.toLowerCase())) {
        alert('Există deja un cont înregistrat cu această adresă de email.');
        createBtn.disabled = false;
        createBtn.textContent = 'Create my account';
        return;
      }

      const newUser = {
        id: Date.now(),
        first, last, email,
        password: pwd, 
        tips: !!document.getElementById('tips').checked
      };
      users.push(newUser);
      saveUsers(users);

      alert('Cont creat cu succes! (Salvat local în browser)');
      form.reset();
      createBtn.disabled = false;
      createBtn.textContent = 'Create my account';
    }, 700);
  });

  document.getElementById('first').value = '';
  document.getElementById('last').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
});
