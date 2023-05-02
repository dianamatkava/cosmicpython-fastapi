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

            } else {
                // All done!
                document.getElementById('applyForm').style.display = 'block'
            } 
        },
        error: function() {
            alert('Unelectable error occurred. Try later')
        }
    })
};


const mediaQueryMin = window.matchMedia('(min-width: 1273px)');

function mediaQueryMinFoo() {

  const form = document.getElementById('form');
  const desc = document.getElementById('desc');
    // desc.appendChild(form) 
  desc.insertBefore(form, desc.firstChild);


  
}

mediaQueryMin.addEventListener('change', function(event) {
  if (event.matches) {
    mediaQueryMinFoo();
  }
});

if (mediaQueryMin.matches) {
    mediaQueryMinFoo();
}



const mediaQueryMax = window.matchMedia('(max-width: 1274px)');

function myFunction() {
    console.log('MOB');
    const form = document.getElementById('form');
    const mob = document.getElementById('mobForm');
    const completed = document.getElementById('completed');
    mob.appendChild(completed) 
    mob.appendChild(form) 
}

mediaQueryMax.addEventListener('change', function(event) {
  if (event.matches) {
    myFunction();
  }
});

if (mediaQueryMax.matches) {
  myFunction();
}