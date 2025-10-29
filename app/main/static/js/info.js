//seleciona cada elemento html por meio do ID. 
const togglePassword = document.querySelector('#togglePassword');//Aqui seleciona o ícone do olho de senha pelo id (togglePassword) da (class="fas fa-eye") definido no html
const password = document.querySelector('#password');//Aqui seleciona o input de senha pelo id (password) definido no html
const toggleCheckPassword = document.querySelector('#toggleCheckPassword');//Aqui seleciona o ícone do olho de checagem de senha pelo id (toggleCheckPassword) da (class="fas fa-eye") definido no html
const checkPassword = document.querySelector('#checkpassword');//Aqui seleciona o input de senha pelo id (checkpassword) definido no html

const register_form = document.querySelector('#register_form') // id do form register



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


// validações antes de enviar o formulário com js

register_form.addEventListener('submit', function (e) {
    e.preventDefault() // impede que a pagina recarregue
    
    let allValid = true;

    const fields = [
        {
            id: 'username',
            validator: nameIsValid
        },
        {
            id: 'email',
            validator: emailIsValid
        },
        {
            id: 'password',
            validator: passwordIsSecure
        },
        {
            id: 'checkpassword',
            validator: passwordMatch
        }
    ]

    const errorIcon = '<i class="fa-solid fa-circle-exclamation"></i>';

    fields.forEach(function (field) {
        const input = document.getElementById(field.id);
        const inputGroup = input.closest('.input-group');
        const inputValue = input.value;       
        
        const errorSpan = inputGroup.querySelector('.error');
        errorSpan.innerHTML = '';

        inputGroup.classList.remove('invalid');
        inputGroup.classList.add('valid');

        const fieldValidator = field.validator(inputValue);
        
        if(!fieldValidator.isValid) {
            errorSpan.innerHTML = `${errorIcon} ${fieldValidator.errorMessage}`;
            inputGroup.classList.add('invalid');
            inputGroup.classList.remove('valid')
            allValid = false;
        }
    })
    
    if(allValid) {
        register_form.submit();
    }

})

function isEmpty(value) {
    return value === '';
}

function nameIsValid(value) {
    const validator = {
        isValid: true,
        errorMessage: null
    };

    if(isEmpty(value)) {
        validator.isValid = false;
        validator.errorMessage = 'O nome é obrigatório!'
        return validator;
    }

    const min = 3;
    if(value.length < min) {
        validator.isValid = false;
        validator.errorMessage = `O nome deve ter no mínimo ${min} caracteres!`
        return validator;
    }

    const regex = /^[\p{L} ]+$/u;
    if(!regex.test(value)) {
        validator.isValid = false;
        validator.errorMessage = 'O nome deve conter apenas letras!'
        return validator;
    }

    return validator
}

function emailIsValid(value) {
    const validator = {
        isValid: true,
        errorMessage: null
    };

    if(isEmpty(value)) {
        validator.isValid = false;
        validator.errorMessage = 'O email é obrigatório!'
        return validator;
    }

    const regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

    if(!regex.test(value)) {
        validator.isValid = false;
        validator.errorMessage = 'O e-mail precisa ser válido!'
        return validator;
    }

    return validator;
}

function passwordIsSecure(value) {
    const validator = {
        isValid: true,
        errorMessage: null
    }

    if (isEmpty(value)) {
        validator.isValid = false;
        validator.errorMessage = 'A senha é obrigatória!';
        return validator;
    }

    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;


    if (!regex.test(value)) {
        validator.isValid = false;
        validator.errorMessage = `
            Sua senha deve conter ao menos: <br/>
            8 dígitos <br/>
            1 letra minúscula <br/>
            1 letra maiúscula  <br/>
            1 número </br>
            1 caractere especial!
        `;
        return validator;
    }

    return validator;
}

function passwordMatch(value) {
    const validator = {
        isValid: true,
        errorMessage: null
    }

    const passwordValue = document.getElementById('password').value;

    if(value === '' || passwordValue !== value) {
        validator.isValid = false;
        validator.errorMessage = 'Senhas não condizem!';
        return validator;
    }

    return validator;
}
