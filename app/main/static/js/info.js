//seleciona cada elemento html por meio do ID. 
const togglePassword = document.querySelector('#togglePassword');//Aqui seleciona o ícone do olho de senha pelo id (togglePassword) da (class="fas fa-eye") definido no html
const password = document.querySelector('#password');//Aqui seleciona o input de senha pelo id (password) definido no html
const toggleCheckPassword = document.querySelector('#toggleCheckPassword');//Aqui seleciona o ícone do olho de checagem de senha pelo id (toggleCheckPassword) da (class="fas fa-eye") definido no html
const checkPassword = document.querySelector('#checkpassword');//Aqui seleciona o input de senha pelo id (checkpassword) definido no html

//Adiciona uma função, escutador de eventos,  que é executada quando o ícone do olho principal (togglePassword) é clicado.
togglePassword.addEventListener('click', function () {
    const type = password.type === 'password' ? 'text' : 'password';
    password.type = type;

    //This = elemento (ou seja, this dentro de um evento é o elemento, que no caso é o olho)
    this.classList.toggle('fa-eye');//olho normal
    this.classList.toggle('fa-eye-slash');//olho cortado
});

//Adiciona uma função, escutador de eventos,  que é executada quando o ícone do olho principal (toggleCheckPassword) é clicado.
toggleCheckPassword.addEventListener('click', function () {
    const type = checkPassword.type === 'password' ? 'text' : 'password';
    checkPassword.type = type;

    //This = elemento (ou seja, this dentro de um evento é o elemento, que no caso é o olho)
    this.classList.toggle('fa-eye');//olho normal
    this.classList.toggle('fa-eye-slash');//olho cortado
});
