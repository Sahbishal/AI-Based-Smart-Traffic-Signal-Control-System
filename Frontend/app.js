const API_BASE_URL = 'http://localhost:5000/api';

let vehicleChart = null;
let efficiencyChart = null;
let isBackendConnected = false;

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateTime();
    checkBackendConnection();
    loadDashboard();
    setInterval(updateTime, 1000);
    setInterval(loadDashboard, 5000);
    setInterval(updateSignalStates, 2000);
    initCharts();
});

function setupEventListeners() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            navBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const tabName = e.target.getAttribute('data-tab');
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName).classList.add('active');
            
            if (tabName === 'analytics') {
                updateCharts();
            }
        });
    });
}

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, { timeout: 3000 });
        if (response.ok) {
            isBackendConnected = true;
            document.getElementById('system-status').textContent = '● Online';
            document.getElementById('system-status').style.color = '#4CAF50';
        }
    } catch (error) {
        isBackendConnected = false;
        document.getElementById('system-status').textContent = '● Offline (Demo Mode)';
        document.getElementById('system-status').style.color = '#ff9800';
        console.warn('Backend offline - using demo data');
    }
}

function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleTimeString();
}

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/overview`);
        if (!response.ok) throw new Error('API Error');
        
        const data = await response.json();
        
        document.getElementById('active-intersections').textContent = data.intersections || 0;
        document.getElementById('system-health').textContent = '100%';
        
        let totalVehicles = 0;
        let emergencyVehicles = 0;
        
        if (data.intersection_statuses) {
            data.intersection_statuses.forEach(status => {
                Object.values(status.vehicle_counts || {}).forEach(count => {
                    totalVehicles += count;
                });
                if (status.emergency_mode) {
                    emergencyVehicles++;
                }
            });
        }
        
        document.getElementById('total-vehicles').textContent = totalVehicles;
        document.getElementById('emergency-vehicles').textContent = emergencyVehicles;
        
        loadIntersections();
    } catch (error) {
        console.warn('Using demo data - Backend unavailable');
        useDemoData();
    }
}

function useDemoData() {
    document.getElementById('active-intersections').textContent = '3';
    document.getElementById('total-vehicles').textContent = Math.floor(Math.random() * 200 + 150);
    document.getElementById('emergency-vehicles').textContent = Math.floor(Math.random() * 3);
    document.getElementById('system-health').textContent = '98%';
    
    const demoIntersections = [
        { id: 'INT_001', name: 'Main Street & 5th Avenue', latitude: 40.7128, longitude: -74.0060, cameras: { north: 'CAM_N1', south: 'CAM_S1', east: 'CAM_E1', west: 'CAM_W1' } },
        { id: 'INT_002', name: 'Park Avenue & Madison', latitude: 40.7150, longitude: -74.0080, cameras: { north: 'CAM_N2', south: 'CAM_S2' } },
        { id: 'INT_003', name: 'Broadway & 42nd Street', latitude: 40.7580, longitude: -73.9855, cameras: { north: 'CAM_N3', south: 'CAM_S3', east: 'CAM_E3' } }
    ];
    
    const container = document.getElementById('intersections-container');
    if (container) {
        container.innerHTML = demoIntersections.map(intersection => `
            <div class="intersection-item">
                <h3>${intersection.name}</h3>
                <p><strong>ID:</strong> ${intersection.id}</p>
                <p><strong>Location:</strong> ${intersection.latitude.toFixed(4)}, ${intersection.longitude.toFixed(4)}</p>
                <p><strong>Cameras:</strong> ${Object.keys(intersection.cameras).join(', ')}</p>
            </div>
        `).join('');
    }
}

async function loadIntersections() {
    try {
        const response = await fetch(`${API_BASE_URL}/intersections`);
        const intersections = await response.json();
        
        const container = document.getElementById('intersections-container');
        container.innerHTML = '';
        
        intersections.forEach(intersection => {
            const item = document.createElement('div');
            item.className = 'intersection-item';
            item.innerHTML = `
                <h3>${intersection.name}</h3>
                <p><strong>ID:</strong> ${intersection.id}</p>
                <p><strong>Location:</strong> ${intersection.latitude.toFixed(4)}, ${intersection.longitude.toFixed(4)}</p>
                <p><strong>Cameras:</strong> ${Object.keys(intersection.cameras).join(', ')}</p>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading intersections:', error);
    }
}

async function updateSignalStates() {
    try {
        const response = await fetch(`${API_BASE_URL}/intersection/INT_001/signal/state`);
        const data = await response.json();
        
        const directions = ['north', 'south', 'east', 'west'];
        directions.forEach(direction => {
            const state = data.signals[direction] || 'red';
            updateTrafficLight(direction, state);
        });
    } catch (error) {
        if (!isBackendConnected) {
            updateDemoSignalStates();
        }
    }
}

function updateDemoSignalStates() {
    const states = ['red', 'yellow', 'green'];
    const directions = ['north', 'south', 'east', 'west'];
    
    directions.forEach(direction => {
        const randomState = states[Math.floor(Math.random() * states.length)];
        updateTrafficLight(direction, randomState);
        
        const vehicleCount = Math.floor(Math.random() * 25 + 3);
        const countElement = document.getElementById(`${direction}-count`);
        if (countElement) {
            countElement.textContent = `${vehicleCount} vehicles`;
        }
    });
}

function updateTrafficLight(direction, state) {
    const lights = {
        'red': document.getElementById(`${direction}-red`),
        'yellow': document.getElementById(`${direction}-yellow`),
        'green': document.getElementById(`${direction}-green`)
    };
    
    Object.values(lights).forEach(light => light.classList.remove('active'));
    
    if (lights[state]) {
        lights[state].classList.add('active');
    }
}

async function triggerEmergency(direction) {
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Processing...';
    button.disabled = true;
    
    try {
        const response = await fetch(
            `${API_BASE_URL}/intersection/INT_001/emergency/${direction}`,
            { method: 'POST' }
        );
        const data = await response.json();
        button.textContent = '✓ Activated!';
        button.style.backgroundColor = '#4CAF50';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
        updateSignalStates();
    } catch (error) {
        console.error('Error triggering emergency:', error);
        button.textContent = '✗ Error!';
        button.style.backgroundColor = '#f44336';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
        if (isBackendConnected === false) {
            alert('Backend offline - Demo mode: Emergency activated for ' + direction);
        }
    }
}

async function analyzeImage() {
    const fileInput = document.getElementById('image-upload');
    const file = fileInput.files[0];
    const resultDiv = document.getElementById('detection-result');
    const button = event.target;
    const originalText = button.textContent;
    
    if (!file) {
        alert('Please select an image');
        return;
    }
    
    button.textContent = 'Analyzing...';
    button.disabled = true;
    resultDiv.textContent = 'Processing image...';
    
    const formData = new FormData();
    formData.append('image', file);
    formData.append('intersection_id', 'INT_001');
    formData.append('direction', 'north');
    
    try {
        const response = await fetch(`${API_BASE_URL}/detection/image`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        resultDiv.innerHTML = `
            <div style="width: 100%; text-align: left;">
                <h4>Detection Results</h4>
                <p><strong>Total Vehicles:</strong> ${data.total_vehicles}</p>
                <p><strong>Emergency Vehicles:</strong> ${data.emergency_vehicles}</p>
                <p><strong>Emergency Types:</strong> ${data.emergency_types.join(', ') || 'None'}</p>
                <h5>Vehicle Breakdown:</h5>
                <ul>
                    ${Object.entries(data.vehicle_breakdown).map(([type, count]) => 
                        `<li>${type}: ${count}</li>`
                    ).join('')}
                </ul>
                <h5>Detections:</h5>
                <ul>
                    ${data.detections.map(d => 
                        `<li>${d.class} (${(d.confidence * 100).toFixed(1)}%) ${d.is_emergency ? '🚨' : ''}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
        button.textContent = '✓ Done!';
    } catch (error) {
        console.error('Error analyzing image:', error);
        if (isBackendConnected === false) {
            const demoResult = Math.floor(Math.random() * 8 + 5);
            resultDiv.innerHTML = `
                <div style="width: 100%; text-align: left;">
                    <h4>Detection Results (Demo Mode)</h4>
                    <p><strong>Total Vehicles:</strong> ${demoResult}</p>
                    <p><strong>Emergency Vehicles:</strong> ${Math.floor(Math.random() * 2)}</p>
                    <p><strong>Emergency Types:</strong> Ambulance</p>
                    <h5>Vehicle Breakdown:</h5>
                    <ul>
                        <li>Car: ${Math.floor(demoResult * 0.6)}</li>
                        <li>Bus: ${Math.floor(demoResult * 0.2)}</li>
                        <li>Truck: ${Math.floor(demoResult * 0.2)}</li>
                    </ul>
                </div>
            `;
            button.textContent = '✓ Done (Demo)!';
        } else {
            button.textContent = '✗ Error!';
            resultDiv.textContent = 'Failed to analyze image';
        }
    }
    
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}

function initCharts() {
    const vehicleCtx = document.getElementById('vehicle-chart');
    const efficiencyCtx = document.getElementById('efficiency-chart');
    
    if (vehicleCtx) {
        vehicleChart = new Chart(vehicleCtx, {
            type: 'doughnut',
            data: {
                labels: ['Cars', 'Trucks', 'Buses', 'Motorcycles', 'Bicycles'],
                datasets: [{
                    data: [450, 120, 80, 150, 45],
                    backgroundColor: [
                        '#2196F3',
                        '#4CAF50',
                        '#ff9800',
                        '#f44336',
                        '#9C27B0'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                }
            }
        });
    }
    
    if (efficiencyCtx) {
        efficiencyChart = new Chart(efficiencyCtx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                datasets: [{
                    label: 'Signal Efficiency (%)',
                    data: [65, 75, 85, 72, 80, 88, 90],
                    borderColor: '#2196F3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    y: {
                        grid: { color: '#444' },
                        ticks: { color: '#aaa' },
                        max: 100
                    },
                    x: {
                        grid: { color: '#444' },
                        ticks: { color: '#aaa' }
                    }
                }
            }
        });
    }
}

function updateCharts() {
    if (vehicleChart) vehicleChart.update();
    if (efficiencyChart) efficiencyChart.update();
}

async function clearEmergency() {
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Clearing...';
    button.disabled = true;
    
    try {
        const response = await fetch(
            `${API_BASE_URL}/intersection/INT_001/emergency/clear`,
            { method: 'POST' }
        );
        button.textContent = '✓ Cleared!';
        button.style.backgroundColor = '#4CAF50';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
    } catch (error) {
        console.error('Error clearing emergency:', error);
        button.textContent = '✓ Cleared (Demo)!';
        button.style.backgroundColor = '#4CAF50';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
    }
}

async function optimizeSignals() {
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Optimizing...';
    button.disabled = true;
    
    try {
        const response = await fetch(
            `${API_BASE_URL}/intersection/INT_001/optimize`,
            { method: 'POST' }
        );
        button.textContent = '✓ Optimized!';
        button.style.backgroundColor = '#4CAF50';
        updateSignalStates();
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
    } catch (error) {
        console.error('Error optimizing signals:', error);
        button.textContent = '✓ Optimized (Demo)!';
        button.style.backgroundColor = '#4CAF50';
        updateDemoSignalStates();
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.disabled = false;
        }, 2000);
    }
}
