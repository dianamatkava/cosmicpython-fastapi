const langButton = document.getElementById('lang-options');
const langDropdown = document.getElementById('lang-dropdown');

langButton.addEventListener('click', () => {
  langDropdown.classList.toggle('hidden');
});


function openForm() {
    const form = document.getElementById('form');   
    const details = document.getElementById('details'); 
    const showDesc = document.getElementById('showDesc'); 
    form.style.display = 'block'
    details.style.display = 'none'
    showDesc.style.display = 'block'
}

function showDesc() {
    const form = document.getElementById('form');   
    const details = document.getElementById('details'); 
    const showDesc = document.getElementById('showDesc'); 
    form.style.display = 'none'
    details.style.display = 'block'
}

var inputs = document.querySelectorAll('input[type="text"]');
var submitButton = document.getElementById('applyFormBtn');

inputs.forEach(function(input) {
    input.addEventListener('input', function() {
        var isFilled = true;
        
        inputs.forEach(function(input) {
            if (input.value.trim() === '') {
                isFilled = false;
            }
        });
        console.log(isFilled)
        if (isFilled) {
            submitButton.removeAttribute('disabled');
        } else {
            submitButton.setAttribute('disabled', 'disabled');
        }
    });
});

function submitSuccess() {
    document.getElementById('applyForm').style.display = 'none'
    document.getElementById('form').style.display = 'none'
    document.getElementById('completed').style.display = 'block'
}

function applyForm() {
    var inputs = document.querySelectorAll('input[type="text"]');
    var res = {}
    for (let input of inputs) {
        res[input.name] = input.value
    }
    $.ajax ({
        type: 'POST',
        url: '/',
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify(res),
        success: function(data) {
            if (data) {
                // Validation failed
                errorEl = document.getElementById('errorMessage');
                errorEl.innerHTML = data['message'];
                errorEl.style.display = 'block';
                document.getElementById('applyForm').style.display = 'block'

            } else {
                // All done!
                document.getElementById('applyForm').style.display = 'block'
            }
            console.log(data)   
        },
        error: function() {
            alert('Unelectable error occurred. Try later')
        }
    })
}