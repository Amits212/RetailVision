document.addEventListener('DOMContentLoaded', function() {
    const userFields = document.getElementById('user-fields');
    const companyFields = document.getElementById('company-fields');
    const signupAsSelect = document.getElementById('signup-as');

    function toggleFields() {
        const companyNameField = companyFields.querySelector('input[name="name"]');
        const companyDescriptionField = companyFields.querySelector('textarea[name="description"]');
        const userFieldInputs = userFields.querySelectorAll('input');

        if (signupAsSelect.value === 'user') {
            userFields.style.display = 'block';
            companyFields.style.display = 'none';
            companyNameField.removeAttribute('required');
            companyDescriptionField.removeAttribute('required');
            userFieldInputs.forEach(input => input.setAttribute('required', 'true'));
        } else if (signupAsSelect.value === 'company') {
            userFields.style.display = 'none';
            companyFields.style.display = 'block';
            companyNameField.setAttribute('required', 'true');
            companyDescriptionField.setAttribute('required', 'true');
            userFieldInputs.forEach(input => input.removeAttribute('required'));
        }
    }

    signupAsSelect.addEventListener('change', toggleFields);

    // Initial toggle on page load
    toggleFields();
});

document.getElementById('signup-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const signupAs = formData.get('signup_as');

    let endpoint = '';
    let data = {};

    if (signupAs === 'user') {
        endpoint = '/api/signup';
        data = {
            username: formData.get('username'),
            password: formData.get('password'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            address: formData.get('address'),
            email: formData.get('email')
        };
    } else if (signupAs === 'company') {
        endpoint = '/api/companysignup';
        data = {
            username: formData.get('username'),
            password: formData.get('password'),
            company: {
                name: formData.get('name'),
                description: formData.get('description')
            }
        };
    }

    console.log('Sending data to:', endpoint, data); // Debugging line

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert(result.message);
});
