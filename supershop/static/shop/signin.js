document.getElementById('id_username').placeholder = "Логин";
document.getElementById('id_password').placeholder = "Пароль";

function showPassword() {
    $('#id_password').wrap("<div class = 'password-area'></div>");
    $('#id_password').after("<div class='show-password fas fa-eye-slash'></div>");
    document.querySelector(".show-password").addEventListener("click", 
    function() { 
        if(this.classList[2] == "fa-eye-slash") {
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
            $('#id_password').attr('type', 'text');
        }
            else {
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
            $('#id_password').attr('type', 'password');
            }
    });
}

if($('input').is('#id_confirm_password')) {
    document.getElementById('id_confirm_password').placeholder = "Повторите пароль";
    document.getElementById('id_first_name').placeholder = "Имя";
    document.getElementById('id_last_name').placeholder = "Фамилия";
    document.getElementById('id_phone').placeholder = "Телефон";
    document.getElementById('id_address').placeholder = "Адрес проживания";
    document.getElementById('id_email').placeholder = "Адрес электронной почты";
    $('#id_email').after("<div class='form-area footer'><span class='politics-text'>Создавая аккаунт, ты принимаешь <div class='condition'><span class = 'conditions'>Политику конфиденциальности</span><span> и </span><span class = 'conditions'>Условия</span></div>нашего магазина</span></div>");
    showPassword();
    $('#id_confirm_password').wrap("<div class = 'password-area'></div>");
    $('#id_confirm_password').after("<div class='show-confirm__password fas fa-eye-slash'></div>");
    document.querySelector(".show-confirm__password").addEventListener("click", 
    function() { 
        if(this.classList[2] == "fa-eye-slash") {
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
            $('#id_confirm_password').attr('type', 'text');
        }
            else {
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
            $('#id_confirm_password').attr('type', 'password');
            }
    });
}
else {
    showPassword();
    $('.auth-container button').on('click', function(){
        $('.wrong-text').show();
        setTimeout(function(){
            $('.wrong-text').css('display', 'block');
            $('.wrong-text').hide('slow');
        }, 3000);

    });
}



