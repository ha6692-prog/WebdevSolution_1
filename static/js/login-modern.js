// Login Modern JavaScript

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const passwordIcon = document.getElementById('passwordIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.textContent = 'visibility_off';
    } else {
        passwordInput.type = 'password';
        passwordIcon.textContent = 'visibility';
    }
}

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showError(fieldId, message) {
    const errorElement = document.getElementById(fieldId + 'Error');
    const inputElement = document.getElementById(fieldId);

    errorElement.textContent = message;
    inputElement.style.borderColor = 'var(--error)';
}

function clearError(fieldId) {
    const errorElement = document.getElementById(fieldId + 'Error');
    const inputElement = document.getElementById(fieldId);

    errorElement.textContent = '';
    inputElement.style.borderColor = 'var(--border)';
}

function showAlert(message) {
    const alertElement = document.getElementById('errorAlert');
    const messageElement = document.getElementById('errorMessage');

    messageElement.textContent = message;
    alertElement.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertElement.style.display = 'none';
    }, 5000);
}

function hideAlert() {
    const alertElement = document.getElementById('errorAlert');
    alertElement.style.display = 'none';
}

// Handle form submission
const loginForm = document.getElementById('loginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');
const btnIcon = document.getElementById('btnIcon');
const spinner = document.getElementById('spinner');

loginForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Clear previous errors
    clearError('email');
    clearError('password');
    hideAlert();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    let isValid = true;

    // Validate email
    if (!email) {
        showError('email', 'Email is required');
        isValid = false;
    } else if (!validateEmail(email)) {
        showError('email', 'Please enter a valid email address');
        isValid = false;
    }

    // Validate password
    if (!password) {
        showError('password', 'Password is required');
        isValid = false;
    } else if (password.length < 6) {
        showError('password', 'Password must be at least 6 characters');
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Signing In...';
    btnIcon.style.display = 'none';
    spinner.style.display = 'inline-block';

    // Submit the form (Django will handle the actual authentication)
    // For now, we'll submit normally. You can also use fetch/AJAX here
    try {
        // If you want to use AJAX instead of normal form submission:
        // const formData = new FormData(loginForm);
        // const response = await fetch('/login', {
        //     method: 'POST',
        //     body: formData,
        //     headers: {
        //         'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        //     }
        // });
        // const data = await response.json();
        // if (data.success) {
        //     window.location.href = data.redirect;
        // } else {
        //     showAlert(data.error || 'Invalid credentials');
        // }

        // For normal form submission (Django handles everything):
        loginForm.submit();
    } catch (error) {
        showAlert('An error occurred. Please try again.');
        // Reset button state
        submitBtn.disabled = false;
        btnText.textContent = 'Sign In';
        btnIcon.style.display = 'inline-block';
        spinner.style.display = 'none';
    }
});

// Clear error on input
document.getElementById('email').addEventListener('input', function () {
    clearError('email');
});

document.getElementById('password').addEventListener('input', function () {
    clearError('password');
});

// Handle social login buttons (placeholder)
document.querySelectorAll('.btn-social').forEach(button => {
    button.addEventListener('click', function () {
        const provider = this.classList.contains('btn-google') ? 'Google' : 'Facebook';
        alert(`${provider} login coming soon!`);
    });
});