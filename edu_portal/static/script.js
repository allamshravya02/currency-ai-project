// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5001';

// Search form submission
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = document.getElementById('search-input').value.trim();
    
    if (!query) {
        showError('Please enter a search term');
        return;
    }
    
    await searchCurrency(query);
});

// Quick search function
function quickSearch(query) {
    document.getElementById('search-input').value = query;
    searchCurrency(query);
}

// Main search function
async function searchCurrency(query) {
    // Show loading, hide results and errors
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    try {
        const response = await fetch(`${API_BASE_URL}/education?query=${encodeURIComponent(query)}`);
        
        if (response.status === 404) {
            throw new Error('Currency not found. Try searching by ISO code (USD, INR), currency name, or country.');
        }
        
        if (!response.ok) {
            throw new Error('Failed to fetch currency information. Please try again.');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Display results
function displayResults(data) {
    // Currency Images
    if (data.images) {
        document.getElementById('note-image').src = `/static/images/${data.images.note || 'placeholder-note.png'}`;
        document.getElementById('coin-image').src = `/static/images/${data.images.coin || 'placeholder-coin.png'}`;
    }

    // Basic Information
    document.getElementById('currency-name').textContent = data.currency_name || 'N/A';
    document.getElementById('iso-code').textContent = data.iso_code || 'N/A';
    document.getElementById('symbol').textContent = data.symbol || 'N/A';
    document.getElementById('country').textContent = data.country || 'N/A';
    document.getElementById('continent').textContent = data.continent || 'N/A';
    document.getElementById('pronunciation').textContent = data.pronunciation || 'N/A';
    
    // Monetary System
    document.getElementById('currency-type').textContent = data.currency_type || 'N/A';
    document.getElementById('issuing-authority').textContent = data.issuing_authority || 'N/A';
    document.getElementById('central-bank').textContent = data.central_bank || 'N/A';
    document.getElementById('usage').textContent = data.usage || 'Information not available';
    document.getElementById('global-importance').textContent = data.global_importance || 'Information not available';
    
    // Denominations - Banknotes
    const banknotesContainer = document.getElementById('banknotes');
    banknotesContainer.innerHTML = '';
    if (data.denominations && data.denominations.notes && data.denominations.notes.length > 0) {
        data.denominations.notes.forEach(note => {
            const badge = document.createElement('span');
            badge.className = 'denomination-badge';
            badge.textContent = `${data.symbol || ''}${note}`;
            banknotesContainer.appendChild(badge);
        });
    } else {
        banknotesContainer.textContent = 'No data available';
    }
    
    // Denominations - Coins
    const coinsContainer = document.getElementById('coins');
    coinsContainer.innerHTML = '';
    if (data.denominations && data.denominations.coins && data.denominations.coins.length > 0) {
        data.denominations.coins.forEach(coin => {
            const badge = document.createElement('span');
            badge.className = 'denomination-badge';
            badge.textContent = `${data.symbol || ''}${coin}`;
            coinsContainer.appendChild(badge);
        });
    } else {
        coinsContainer.textContent = 'No data available';
    }
    
    // Facts
    const factsList = document.getElementById('facts-list');
    factsList.innerHTML = '';
    if (data.facts && data.facts.length > 0) {
        data.facts.forEach(fact => {
            const li = document.createElement('li');
            li.textContent = fact;
            factsList.appendChild(li);
        });
    } else {
        factsList.innerHTML = '<li style="border: none;">No facts available</li>';
    }
    
    // Recognition Tips
    const recognitionList = document.getElementById('recognition-tips-list');
    recognitionList.innerHTML = '';
    if (data.recognition_tips && data.recognition_tips.length > 0) {
        data.recognition_tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            recognitionList.appendChild(li);
        });
    } else {
        recognitionList.innerHTML = '<li style="border: none;">No recognition tips available</li>';
    }
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
    
    // Smooth scroll to results
    document.getElementById('results').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Show error
function showError(message) {
    const errorElement = document.getElementById('error');
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
}

// Initialize
console.log('Education Portal initialized');
console.log('Backend URL:', API_BASE_URL);