document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');
    const userTypeRadios = document.querySelectorAll('input[name="user-type"]');
    const loginTypeRadios = document.querySelectorAll('input[name="login-type"]');
    const userSignupDiv = document.getElementById('user-signup');
    const companySignupDiv = document.getElementById('company-signup');
    const contentDiv = document.getElementById('content');
    const companyListDiv = document.getElementById('company-list');
    const insightsDiv = document.getElementById('insights');
    const insightsChartCtx = document.getElementById('insights-chart').getContext('2d');
    let insightsChart;

    userTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'company') {
                userSignupDiv.style.display = 'none';
                companySignupDiv.style.display = 'block';
            } else {
                userSignupDiv.style.display = 'block';
                companySignupDiv.style.display = 'none';
            }
        });
    });

    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userType = document.querySelector('input[name="user-type"]:checked').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (userType === 'company') {
            const companyName = document.getElementById('company-name').value;
            const companyDescription = document.getElementById('company-description').value;
            const companyImage = document.getElementById('company-image').value;

            await fetch('/api/companysignup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    password,
                    company: {
                        name: companyName,
                        description: companyDescription,
                        image: companyImage
                    }
                })
            });
        } else {
            const firstName = document.getElementById('first-name').value;
            const lastName = document.getElementById('last-name').value;
            const address = document.getElementById('address').value;
            const email = document.getElementById('email').value;

            await fetch('/api/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, first_name: firstName, last_name: lastName, address, email })
            });
        }

        alert('Sign up successful');
    });

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const loginType = document.querySelector('input[name="login-type"]:checked').value;
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        const response = await fetch(loginType === 'company' ? '/api/companylogin' : '/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            contentDiv.style.display = 'block';
            if (loginType === 'company') {
                insightsDiv.style.display = 'block';
                fetchProductInsights();
            } else {
                fetchCompanies();
            }
        } else {
            alert('Login failed');
        }
    });

    async function fetchCompanies() {
        const response = await fetch('/api/companies');
        const companies = await response.json();
        companyListDiv.innerHTML = '';

        companies.forEach(company => {
            const companyDiv = document.createElement('div');
            companyDiv.textContent = company.name;
            companyDiv.addEventListener('click', () => fetchCompanyProducts(company.id));
            companyListDiv.appendChild(companyDiv);
        });
    }

    async function fetchCompanyProducts(companyId) {
        const response = await fetch(`/api/${companyId}/products`);
        const products = await response.json();
        companyListDiv.innerHTML = '';

        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.textContent = `${product.name} - $${product.price}`;
            const purchaseButton = document.createElement('button');
            purchaseButton.textContent = 'Purchase';
            purchaseButton.addEventListener('click', () => makePurchase(product));
            productDiv.appendChild(purchaseButton);
            companyListDiv.appendChild(productDiv);
        });
    }

    async function makePurchase(product) {
        const userId = 'current-user-id'; // Replace with the actual user ID
        const companyId = 'company-id'; // Replace with the actual company ID

        await fetch('/api/purchases', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                company_id: companyId,
                products: [product]
            })
        });

        alert('Purchase successful');
    }

    async function fetchProductInsights() {
        const companyId = 'company-id'; // Replace with the actual company ID
        const response = await fetch(`/api/companies/${companyId}/insights`);
        const insights = await response.json();

        if (insightsChart) {
            insightsChart.destroy();
        }

        insightsChart = new Chart(insightsChartCtx, {
            type: 'bar',
            data: {
                labels: insights.map(i => i.name),
                datasets: [{
                    label: '# of Purchases',
                    data: insights.map(i => i.purchase_count),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1
