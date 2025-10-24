// weather_app/app.js
// Beginner version: uses mock data so no API key required.
// To use a real API (OpenWeatherMap), see notes below.

const sampleData = {
  "Delhi": { temp: 30, desc: "Sunny", humidity: 40 },
  "Mumbai": { temp: 28, desc: "Partly cloudy", humidity: 70 },
  "Chennai": { temp: 32, desc: "Humid", humidity: 75 }
};

function showResult(city, data) {
  const r = document.getElementById("result");
  r.innerHTML = `
    <h2>${city}</h2>
    <p>Temperature: ${data.temp}°C</p>
    <p>Condition: ${data.desc}</p>
    <p>Humidity: ${data.humidity}%</p>
  `;
}

function showError(msg) {
  const r = document.getElementById("result");
  r.innerHTML = `<p class="hint">${msg}</p>`;
}

document.getElementById("search").addEventListener("click", () => {
  const city = document.getElementById("city").value.trim();
  if (!city) {
    showError("Please enter a city.");
    return;
  }

  // Beginner: use sample data
  const key = Object.keys(sampleData).find(k => k.toLowerCase() === city.toLowerCase());
  if (key) {
    showResult(key, sampleData[key]);
    return;
  } else {
    showError("No data in sample. Try Delhi / Mumbai / Chennai or follow README to add an API key.");
  }
});

/* --- Optional: to use OpenWeatherMap API ---
Uncomment the fetch call and add your API key. Replace YOUR_API_KEY with your key.

fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=YOUR_API_KEY`)
  .then(resp => resp.json())
  .then(data => {
     if (data.cod !== 200) return showError("City not found");
     const mapped = { temp: Math.round(data.main.temp), desc: data.weather[0].description, humidity: data.main.humidity };
     showResult(data.name, mapped);
  })
  .catch(err => showError("Network error"));
*/
