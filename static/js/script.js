/* Smart Kitchen Garden Management System - JavaScript */

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Smart Kitchen Garden System Loaded');
    initializeSearch();
    initializeFilters();
});

// Initialize search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', debounce(function(e) {
            const searchTerm = e.target.value.trim();
            if (searchTerm.length > 0) {
                performSearch(searchTerm);
            }
        }, 300));
    }
}

// Initialize filter functionality
function initializeFilters() {
    const seasonBtns = document.querySelectorAll('.season-btn');
    seasonBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            seasonBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Debounce function to limit API calls
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Perform plant search
function performSearch(searchTerm) {
    fetch(`/api/search?q=${encodeURIComponent(searchTerm)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Search failed');
            }
            return response.json();
        })
        .then(data => {
            updateSearchResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Search failed. Please try again.', 'error');
        });
}

// Update search results on the page
function updateSearchResults(results) {
    const plantsGrid = document.querySelector('.plants-grid');
    if (!plantsGrid) return;

    if (results.length === 0) {
        plantsGrid.innerHTML = '<p>No plants found matching your search.</p>';
        return;
    }

    let html = '';
    results.forEach(plant => {
        html += `
            <div class="plant-card">
                <div class="plant-image">🌱</div>
                <h3>${plant.name}</h3>
                <p class="description">${plant.description}</p>
                <a href="/plant/${plant.id}" class="btn btn-small">View Details</a>
            </div>
        `;
    });

    plantsGrid.innerHTML = html;
}

// Fetch and display plants by season
function fetchPlantsBySeason(season) {
    fetch(`/api/plants/season/${encodeURIComponent(season)}`)
        .then(response => response.json())
        .then(data => {
            updatePlantsDisplay(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to load plants. Please try again.', 'error');
        });
}

// Update plants display
function updatePlantsDisplay(plants) {
    const plantsGrid = document.querySelector('.plants-grid');
    if (!plantsGrid) return;

    if (plants.length === 0) {
        plantsGrid.innerHTML = '<p>No plants available for this season.</p>';
        return;
    }

    let html = '';
    plants.forEach(plant => {
        html += `
            <div class="plant-card">
                <div class="plant-image">🌱</div>
                <h3>${plant.name}</h3>
                <div class="plant-info">
                    <span class="season">${plant.best_season}</span>
                    <span class="sunlight">☀️ ${plant.sunlight_hours}h</span>
                </div>
                <a href="/plant/${plant.id}" class="btn btn-small">View Details</a>
            </div>
        `;
    });

    plantsGrid.innerHTML = html;
}

// Fetch plant care schedule
function fetchPlantSchedule(plantId) {
    fetch(`/api/schedule/${plantId}`)
        .then(response => response.json())
        .then(data => {
            displaySchedule(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Display plant care schedule
function displaySchedule(schedules) {
    const scheduleContainer = document.querySelector('.schedule-container');
    if (!scheduleContainer) return;

    if (schedules.length === 0) {
        scheduleContainer.innerHTML = '<p>No schedule data available.</p>';
        return;
    }

    let html = '<h3>Care Schedule</h3>';
    html += '<ul>';
    schedules.forEach(schedule => {
        html += `
            <li>
                <strong>${schedule.task}</strong>
                <br>Frequency: ${schedule.frequency}
                <br>Duration: ${schedule.duration}
                <br><em>${schedule.notes}</em>
            </li>
        `;
    });
    html += '</ul>';

    scheduleContainer.innerHTML = html;
}

// Fetch care tips for a plant
function fetchCareTips(plantId) {
    fetch(`/api/care-tips/${plantId}`)
        .then(response => response.json())
        .then(data => {
            displayCareTips(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Display care tips
function displayCareTips(tips) {
    const tipsContainer = document.querySelector('.care-tips-container');
    if (!tipsContainer) return;

    if (tips.length === 0) {
        tipsContainer.innerHTML = '<p>No care tips available.</p>';
        return;
    }

    let html = '<div class="care-tips-list">';
    tips.forEach(tip => {
        const priorityClass = `priority-${tip.priority.toLowerCase()}`;
        html += `
            <div class="care-tip ${priorityClass}">
                <strong>${tip.category}</strong> (${tip.priority})
                <p>${tip.tip}</p>
            </div>
        `;
    });
    html += '</div>';

    tipsContainer.innerHTML = html;
}

// Show notification message
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        background: ${type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Fetch all plants
function fetchAllPlants() {
    fetch('/api/plants')
        .then(response => response.json())
        .then(data => {
            console.log('Plants loaded:', data);
        })
        .catch(error => {
            console.error('Error loading plants:', error);
        });
}

// Add plant to user's garden
function addPlantToGarden(plantId) {
    const data = {
        plant_id: plantId,
        planting_date: new Date().toISOString()
    };

    fetch('/api/gardens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
            showNotification(result.message, 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to add plant to garden.', 'error');
    });
}

// Calculate harvest date based on plant and planting date
function calculateHarvestDate(plantId, plantingDate) {
    fetch(`/api/plants/${plantId}`)
        .then(response => response.json())
        .then(plant => {
            const harvestDate = new Date(plantingDate);
            harvestDate.setDate(harvestDate.getDate() + plant.harvest_days);
            return harvestDate;
        })
        .catch(error => console.error('Error:', error));
}

// Export functions for global use
window.fetchPlantsBySeason = fetchPlantsBySeason;
window.addPlantToGarden = addPlantToGarden;
window.fetchCareTips = fetchCareTips;
window.fetchPlantSchedule = fetchPlantSchedule;
window.showNotification = showNotification;
