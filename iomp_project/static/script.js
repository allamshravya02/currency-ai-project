// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// Manual Conversion Form
document.getElementById('manual-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fromCurrency = document.getElementById('from-currency').value;
    const toCurrency = document.getElementById('to-currency').value;
    const amount = parseFloat(document.getElementById('amount').value);

    // Validation
    if (!fromCurrency || !toCurrency || !amount) {
        showError('Please fill all fields');
        return;
    }

    if (fromCurrency === toCurrency) {
        showError('Please select different currencies');
        return;
    }

    // Show loading
    showLoading();
    hideResult();
    hideError();

    try {
        const response = await fetch(`${API_BASE_URL}/convert/manual`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from: fromCurrency,
                to: toCurrency,
                amount: amount
            })
        });

        if (!response.ok) {
            throw new Error('Conversion failed. Please try again.');
        }

        const data = await response.json();
        displayResult(data);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to connect to server. Make sure the server is running on port 5000.');
    } finally {
        hideLoading();
    }
});

// Display Result
function displayResult(data) {
    document.getElementById('result-from').textContent = `${data.from} ${data.amount.toFixed(2)}`;
    document.getElementById('result-to').textContent = data.to;
    document.getElementById('result-amount').textContent = `${data.from} ${data.amount.toFixed(2)}`;
    document.getElementById('result-converted').textContent = `${data.to} ${data.converted_amount.toFixed(2)}`;
    document.getElementById('result-rate').textContent = `1 ${data.from} = ${data.rate.toFixed(6)} ${data.to}`;

    showResult();
}

// Helper Functions
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showResult() {
    document.getElementById('result').classList.remove('hidden');
}

function hideResult() {
    document.getElementById('result').classList.add('hidden');
}

function showError(message) {
    const errorElement = document.getElementById('error');
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

// Initialize
console.log('Manual Currency Converter initialized');
console.log('Backend API:', API_BASE_URL);

