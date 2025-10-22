// Register Modern JavaScript

let currentStep = 0;
const totalSteps = 3;

// Form data object
const formData = {
    email: '',
    password: '',
    confirmPassword: '',
    role: '',
    firstName: '',
    lastName: '',
    phone: '',
    dateOfBirth: '',
    gender: '',
    agreeToTerms: false
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    updateProgress();
    updateNavigationButtons();
});

// Toggle password visibility
function togglePassword(fieldId) {
    const passwordInput = document.getElementById(fieldId);
    const iconId = fieldId + 'Icon';
    const passwordIcon = document.getElementById(iconId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.textContent = 'visibility_off';
    } else {
        passwordInput.type = 'password';
        passwordIcon.textContent = 'visibility';
    }
}

// Validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8 && /(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password);
}

function validatePhone(phone) {
    return /^\+?[\d\s-()]{10,}$/.test(phone);
}

function showError(fieldId, message) {
    const errorElement = document.getElementById(fieldId + 'Error');
    const inputElement = document.getElementById(fieldId);

    if (errorElement) errorElement.textContent = message;
    if (inputElement) inputElement.style.borderColor = 'var(--error)';
}

function clearError(fieldId) {
    const errorElement = document.getElementById(fieldId + 'Error');
    const inputElement = document.getElementById(fieldId);

    if (errorElement) errorElement.textContent = '';
    if (inputElement) inputElement.style.borderColor = 'var(--border)';
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

// Validate current step
function validateStep(step) {
    let isValid = true;

    // Clear all previous errors for the current step
    if (step === 0) {
        clearError('email');
        clearError('password');
        clearError('confirmPassword');
        clearError('role');

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const role = document.getElementById('role').value;

        if (!email) {
            showError('email', 'Email is required');
            isValid = false;
        } else if (!validateEmail(email)) {
            showError('email', 'Please enter a valid email address');
            isValid = false;
        }

        if (!password) {
            showError('password', 'Password is required');
            isValid = false;
        } else if (password.length < 8) {
            showError('password', 'Password must be at least 8 characters');
            isValid = false;
        } else if (!validatePassword(password)) {
            showError('password', 'Password must contain uppercase, lowercase, and number');
            isValid = false;
        }

        if (password !== confirmPassword) {
            showError('confirmPassword', 'Passwords do not match');
            isValid = false;
        }

        if (!role) {
            showError('role', 'Please select your role');
            isValid = false;
        }
    } else if (step === 1) {
        clearError('firstName');
        clearError('lastName');
        clearError('phone');
        clearError('dateOfBirth');
        clearError('gender');

        const firstName = document.getElementById('firstName').value.trim();
        const lastName = document.getElementById('lastName').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const dateOfBirth = document.getElementById('dateOfBirth').value;
        const gender = document.getElementById('gender').value;

        if (!firstName) {
            showError('firstName', 'First name is required');
            isValid = false;
        }

        if (!lastName) {
            showError('lastName', 'Last name is required');
            isValid = false;
        }

        if (!phone) {
            showError('phone', 'Phone number is required');
            isValid = false;
        } else if (!validatePhone(phone)) {
            showError('phone', 'Please enter a valid phone number');
            isValid = false;
        }

        if (!dateOfBirth) {
            showError('dateOfBirth', 'Date of birth is required');
            isValid = false;
        }

        if (!gender) {
            showError('gender', 'Please select your gender');
            isValid = false;
        }
    } else if (step === 2) {
        clearError('agreeToTerms');

        const agreeToTerms = document.getElementById('agreeToTerms').checked;

        if (!agreeToTerms) {
            showError('agreeToTerms', 'You must agree to the terms and conditions');
            isValid = false;
        }
    }

    return isValid;
}

// Update progress bar and step indicator
function updateProgress() {
    const progressFill = document.getElementById('progressFill');
    const stepIndicator = document.getElementById('stepIndicator');
    const percentage = (currentStep / (totalSteps - 1)) * 100;

    progressFill.style.width = percentage + '%';
    stepIndicator.textContent = `Step ${currentStep + 1} of ${totalSteps}`;

    // Update step labels
    document.querySelectorAll('.step-label').forEach((label, index) => {
        if (index === currentStep) {
            label.classList.add('active');
        } else {
            label.classList.remove('active');
        }
    });
}

// Update navigation buttons
function updateNavigationButtons() {
    const backBtn = document.getElementById('backBtn');
    const nextBtn = document.getElementById('nextBtn');
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const socialLogin = document.getElementById('socialLogin');

    // Back button
    backBtn.disabled = currentStep === 0;

    // Next/Submit button
    if (currentStep === totalSteps - 1) {
        btnText.textContent = 'Create Account';
        btnIcon.textContent = 'check_circle';
    } else {
        btnText.textContent = 'Next';
        btnIcon.textContent = 'arrow_forward';
    }

    // Show/hide social login (only on first step)
    if (socialLogin) {
        socialLogin.style.display = currentStep === 0 ? 'block' : 'none';
    }
}

// Show/hide steps
function showStep(step) {
    document.querySelectorAll('.form-step').forEach((stepElement, index) => {
        if (index === step) {
            stepElement.classList.add('active');
        } else {
            stepElement.classList.remove('active');
        }
    });
}

// Save form data before moving steps
function saveCurrentStepData() {
    if (currentStep === 0) {
        formData.email = document.getElementById('email').value.trim();
        formData.password = document.getElementById('password').value;
        formData.confirmPassword = document.getElementById('confirmPassword').value;
        formData.role = document.getElementById('role').value;
    } else if (currentStep === 1) {
        formData.firstName = document.getElementById('firstName').value.trim();
        formData.lastName = document.getElementById('lastName').value.trim();
        formData.phone = document.getElementById('phone').value.trim();
        formData.dateOfBirth = document.getElementById('dateOfBirth').value;
        formData.gender = document.getElementById('gender').value;
    } else if (currentStep === 2) {
        formData.agreeToTerms = document.getElementById('agreeToTerms').checked;
    }
}

// Update summary on step 3
function updateSummary() {
    document.getElementById('summaryName').textContent = `${formData.firstName} ${formData.lastName}`;
    document.getElementById('summaryEmail').textContent = formData.email;
    document.getElementById('summaryRole').textContent = formData.role === 'patient' ? 'Patient' : 'Doctor';
    document.getElementById('summaryPhone').textContent = formData.phone;
}

// Next step
function nextStep() {
    hideAlert();

    if (!validateStep(currentStep)) {
        return;
    }

    saveCurrentStepData();

    if (currentStep === totalSteps - 1) {
        // Submit form
        submitForm();
    } else {
        currentStep++;
        showStep(currentStep);
        updateProgress();
        updateNavigationButtons();

        // Update summary if moving to step 3
        if (currentStep === 2) {
            updateSummary();
        }
    }
}

// Previous step
function previousStep() {
    if (currentStep > 0) {
        saveCurrentStepData();
        currentStep--;
        showStep(currentStep);
        updateProgress();
        updateNavigationButtons();
    }
}

// Submit form
async function submitForm() {
    const submitBtn = document.getElementById('nextBtn');
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const spinner = document.getElementById('spinner');

    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Creating Account...';
    btnIcon.style.display = 'none';
    spinner.style.display = 'inline-block';

    try {
        // Submit the form (Django will handle authentication)
        const form = document.getElementById('registerForm');
        form.submit();

        // If using AJAX instead:
        // const formDataToSend = new FormData(form);
        // const response = await fetch('/register', {
        //     method: 'POST',
        //     body: formDataToSend
        // });
        // const data = await response.json();
        // if (data.success) {
        //     window.location.href = '/login?message=Registration successful';
        // } else {
        //     showAlert(data.error || 'Registration failed');
        // }
    } catch (error) {
        showAlert('An error occurred. Please try again.');
        // Reset button state
        submitBtn.disabled = false;
        btnText.textContent = 'Create Account';
        btnIcon.style.display = 'inline-block';
        spinner.style.display = 'none';
    }
}

// Clear errors on input
document.querySelectorAll('.form-input, .form-select').forEach(input => {
    input.addEventListener('input', function () {
        clearError(this.id);
    });
});

// Handle social login buttons
document.querySelectorAll('.btn-social').forEach(button => {
    button.addEventListener('click', function () {
        const provider = this.classList.contains('btn-google') ? 'Google' : 'Facebook';
        alert(`${provider} registration coming soon!`);
    });
});